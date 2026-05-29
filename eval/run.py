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
    p.add_argument("--models", default=None,
                   help="comma list of models to sweep (overrides --model); prints a comparison table")
    p.add_argument("--task", default="contract_nli", help=f"one of {list(data.TASKS)}")
    p.add_argument("--condition", default="baseline,cli",
                   help="comma list of {baseline,tool,cli}; 'both'=baseline,cli; 'all'=baseline,tool,cli")
    p.add_argument("--data", help="JSONL or TSV dataset (default: built-in sample)")
    p.add_argument("--legalbench", help="real LegalBench task, e.g. contract_nli_sharing_with_employees")
    p.add_argument("--split", default="test", help="dataset split (default: test)")
    p.add_argument("--limit", type=int, default=0, help="max examples (0 = all)")
    p.add_argument("--max-rounds", type=int, default=4, dest="max_rounds")
    p.add_argument("--temperature", type=float, default=0.0)
    p.add_argument("--hypothesis", default=None, help="fixed hypothesis when the data lacks one")
    p.add_argument("--text-col", default="text", dest="text_col")
    p.add_argument("--answer-col", default="answer", dest="answer_col")
    p.add_argument("--hypothesis-col", default=None, dest="hypothesis_col")
    p.add_argument("--out", default=None, help="write per-example JSONL log here")
    return p.parse_args()


def parse_conditions(spec_str):
    aliases = {"both": ["baseline", "cli"], "all": ["baseline", "tool", "cli"]}
    valid = {"baseline", "tool", "cli"}
    conds = []
    for c in spec_str.split(","):
        c = c.strip()
        conds.extend(aliases.get(c, [c]))
    bad = [c for c in conds if c not in valid]
    if bad:
        raise SystemExit(f"unknown condition(s) {bad}; valid: {sorted(valid)} (or both/all)")
    return conds


def evaluate(spec, task, examples, conditions, args, logf):
    """Run every condition over all examples for one model; return per-condition stats."""
    client = models.make_client(spec)
    print(f"\n### model={spec.name} ({spec.provider}:{spec.model_id})  "
          f"examples={len(examples)}  conditions={conditions}")
    stats = {c: {"correct": 0, "total": 0, "tool_calls": 0, "errors": 0} for c in conditions}
    for i, ex in enumerate(examples):
        for c in conditions:
            try:
                if c == "baseline":
                    pred, tr = agents.run_baseline(client, spec, task, ex, args.temperature)
                elif c == "tool":
                    pred, tr = agents.run_tool(client, spec, task, ex, args.max_rounds, args.temperature)
                else:  # cli
                    pred, tr = agents.run_cli(client, spec, task, ex, args.max_rounds, args.temperature)
                err = None
            except Exception as e:  # noqa: BLE001 - keep the sweep going
                pred, tr, err = None, [], str(e)
            ncalls = sum(1 for t in tr if t.get("role") == "tool")
            ok = pred is not None and pred == ex["gold"]
            s = stats[c]
            s["total"] += 1
            s["correct"] += int(ok)
            s["tool_calls"] += ncalls
            s["errors"] += int(err is not None)
            if logf:
                logf.write(json.dumps({
                    "i": i, "condition": c, "model": spec.name, "task": task["name"],
                    "hypothesis": ex["hypothesis"], "gold": ex["gold"], "pred": pred,
                    "correct": ok, "error": err, "n_tool_calls": ncalls, "transcript": tr,
                }) + "\n")
            mark = "OK " if ok else ("ERR" if err else "X  ")
            extra = f" calls={ncalls}" if c in ("tool", "cli") else ""
            print(f"[{i+1}/{len(examples)}] {c:8} {mark} pred={pred} gold={ex['gold']}{extra}"
                  + (f"  ({err[:80]})" if err else ""))
    return stats


def main():
    args = parse_args()
    task = data.get_task(args.task)
    examples = data.load_examples(args, task)
    conditions = parse_conditions(args.condition)
    model_names = [m.strip() for m in (args.models or args.model).split(",") if m.strip()]
    specs = [models.resolve(m) for m in model_names]

    logf = None
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        logf = open(args.out, "w")

    table = {}  # spec.name -> stats
    for spec in specs:
        try:
            table[spec.name] = evaluate(spec, task, examples, conditions, args, logf)
        except SystemExit as e:   # e.g. missing API key — skip this model
            print(f"  ! skipping {spec.name}: {e}")
    if logf:
        logf.close()

    # comparison table
    print(f"\n=== results: task={task['name']}, {len(examples)} examples ===")
    header = "model".ljust(20) + "".join(c.ljust(16) for c in conditions)
    print(header)
    print("-" * len(header))
    for name, stats in table.items():
        row = name.ljust(20)
        for c in conditions:
            s = stats[c]
            acc = s["correct"] / s["total"] if s["total"] else 0.0
            cell = f"{acc:.0%} ({s['correct']}/{s['total']})"
            if s["errors"]:
                cell += f" !{s['errors']}"
            row += cell.ljust(16)
        print(row)
    if any(c in ("tool", "cli") for c in conditions):
        print("\navg reasoner calls (tool/cli conditions):")
        for name, stats in table.items():
            calls = {c: (stats[c]["tool_calls"] / stats[c]["total"] if stats[c]["total"] else 0)
                     for c in conditions if c in ("tool", "cli")}
            print(f"  {name.ljust(20)} " + "  ".join(f"{c}={v:.1f}" for c, v in calls.items()))
    if args.out:
        print(f"\nper-example transcripts -> {args.out}")


if __name__ == "__main__":
    main()
