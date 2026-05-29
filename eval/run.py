#!/usr/bin/env python3
"""Agentic eval harness: compare a model answering LegalBench-style tasks
directly (baseline) vs. with the `deontic` reasoner as a tool (tool).

Run from the project root (so the reasoner path resolves):

  export PATH="$HOME/.elan/bin:$PATH" && lake build deontic   # once
  python eval/run.py --model stub                              # offline smoke test
  python eval/run.py --model gpt-4o-mini --condition both --out runs/gpt4omini.jsonl
  python eval/run.py --model openrouter:deepseek/deepseek-chat --task contract_nli
  python eval/run.py --model gpt-4.1 --data path/to/legalbench_task.tsv --hypothesis "..."

Keys: OPENAI_API_KEY (openai), OPENROUTER_API_KEY (openrouter).
"""
from __future__ import annotations
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import models      # noqa: E402
import data        # noqa: E402
import agents      # noqa: E402


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", default="stub", help="registry name or provider:model_id")
    p.add_argument("--task", default="contract_nli", help=f"one of {list(data.TASKS)}")
    p.add_argument("--condition", choices=["baseline", "tool", "both"], default="both")
    p.add_argument("--data", help="JSONL or TSV dataset (default: built-in sample)")
    p.add_argument("--limit", type=int, default=0, help="max examples (0 = all)")
    p.add_argument("--max-rounds", type=int, default=4, dest="max_rounds")
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--hypothesis", default=None, help="fixed hypothesis when the data lacks one")
    p.add_argument("--text-col", default="text", dest="text_col")
    p.add_argument("--answer-col", default="answer", dest="answer_col")
    p.add_argument("--hypothesis-col", default=None, dest="hypothesis_col")
    p.add_argument("--out", default=None, help="write per-example JSONL log here")
    return p.parse_args()


def main():
    args = parse_args()
    spec = models.resolve(args.model)
    client = models.make_client(spec)
    task = data.get_task(args.task)
    examples = data.load_examples(args, task)
    conditions = ["baseline", "tool"] if args.condition == "both" else [args.condition]

    print(f"model={spec.name} ({spec.provider}:{spec.model_id})  task={task['name']}  "
          f"examples={len(examples)}  conditions={conditions}\n")

    stats = {c: {"correct": 0, "total": 0, "tool_calls": 0} for c in conditions}
    logf = None
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        logf = open(args.out, "w")

    for i, ex in enumerate(examples):
        for c in conditions:
            try:
                if c == "baseline":
                    pred, tr = agents.run_baseline(client, spec, task, ex, args.temperature)
                else:
                    pred, tr = agents.run_tool(client, spec, task, ex, args.max_rounds, args.temperature)
                err = None
            except Exception as e:  # noqa: BLE001 - keep the sweep going
                pred, tr, err = None, [], str(e)
            ncalls = sum(1 for t in tr if t.get("role") == "tool")
            ok = pred is not None and pred == ex["gold"]
            stats[c]["total"] += 1
            stats[c]["correct"] += int(ok)
            stats[c]["tool_calls"] += ncalls
            if logf:
                logf.write(json.dumps({
                    "i": i, "condition": c, "model": spec.name, "task": task["name"],
                    "hypothesis": ex["hypothesis"], "gold": ex["gold"], "pred": pred,
                    "correct": ok, "error": err, "n_tool_calls": ncalls, "transcript": tr,
                }) + "\n")
            mark = "OK " if ok else ("ERR" if err else "X  ")
            extra = f" calls={ncalls}" if c == "tool" else ""
            print(f"[{i+1}/{len(examples)}] {c:8} {mark} pred={pred} gold={ex['gold']}{extra}"
                  + (f"  ({err})" if err else ""))
    if logf:
        logf.close()

    print("\n=== summary ===")
    for c in conditions:
        s = stats[c]
        acc = s["correct"] / s["total"] if s["total"] else 0.0
        tc = f"  avg_tool_calls={s['tool_calls']/s['total']:.1f}" if c == "tool" and s["total"] else ""
        print(f"{spec.name:18} {c:8} accuracy {s['correct']}/{s['total']} = {acc:.1%}{tc}")
    if args.out:
        print(f"\nper-example log -> {args.out}")


if __name__ == "__main__":
    main()
