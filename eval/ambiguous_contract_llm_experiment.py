#!/usr/bin/env python3
"""LLM version of the ambiguous-contract experiment.

The offline sibling (`ambiguous_contract_experiment.py`) compares a text
heuristic, KNN label-voting, and the formal reasoner with *no language model in
the loop*. This script puts real models in the loop and compares three
conditions over the same models:

  baseline : prompt the model directly for Yes/No (no tools, no precedents).
  tool     : give the model the `run_deontic` reasoner; it formalizes the clause
             as a DDL theory and queries it for a few rounds before answering.
  knn      : retrieve the k nearest decided precedents (structured Jaccard over
             template/mode/facts, same as the offline script) and show them to
             the model as few-shot context; it answers with no reasoner.

Use agentic models that understand tool use (gpt-5.4 family, deepseek, grok),
plus an older model (gpt-4o) for contrast. Stratified split gives KNN a
precedent pool disjoint from the evaluated test slice.

  python eval/ambiguous_contract_llm_experiment.py \
    --models gpt-5.4-mini,gpt-4o,openrouter:deepseek/deepseek-chat \
    --limit 90 --k 5 --out eval/runs/ambiguous_llm.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import models      # noqa: E402
import agents      # noqa: E402
import data        # noqa: E402


def load_jsonl(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def vector(row: dict) -> set[str]:
    return {f"template={row['template']}", f"mode={row['mode']}",
            *[f"fact={f}" for f in row["facts"]]}


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a or b else 1.0


def knn_neighbors(train: list[dict], row: dict, k: int) -> list[dict]:
    rv = vector(row)
    scored = sorted(train, key=lambda t: jaccard(vector(t), rv), reverse=True)
    return scored[:k]


def split(rows: list[dict], seed: int, train_frac: float):
    """Stratified by clause family: a precedent pool + a held-out test pool."""
    by_template = defaultdict(list)
    for r in rows:
        by_template[r["template"]].append(r)
    rng = random.Random(seed)
    train, test = [], []
    for group in by_template.values():
        rng.shuffle(group)
        n = max(1, int(round(len(group) * train_frac)))
        train.extend(group[:n])
        test.extend(group[n:])
    rng.shuffle(test)
    return train, test


def stratified_sample(test: list[dict], limit: int, seed: int) -> list[dict]:
    """Pick `limit` test rows balanced across hypothesis modes (may/must/must_not)."""
    if not limit or limit >= len(test):
        return test
    by_mode = defaultdict(list)
    for r in test:
        by_mode[r["mode"]].append(r)
    rng = random.Random(seed)
    for v in by_mode.values():
        rng.shuffle(v)
    out, modes = [], sorted(by_mode)
    i = 0
    while len(out) < limit:
        m = modes[i % len(modes)]
        if by_mode[m]:
            out.append(by_mode[m].pop())
        elif all(not by_mode[mm] for mm in modes):
            break
        i += 1
    rng.shuffle(out)
    return out


def accuracy(rows, preds):
    n = len(rows)
    return sum(p == r["gold"] for p, r in zip(preds, rows)) / n if n else 0.0


def by_group(rows, preds, key):
    g = defaultdict(list)
    for r, p in zip(rows, preds):
        g[r[key]].append(int(p == r["gold"]))
    return {k: sum(v) / len(v) for k, v in sorted(g.items())}


def run_model(spec, task, test, train, k, max_rounds, temperature, conditions, logf):
    client = models.make_client(spec)
    print(f"\n### model={spec.name} ({spec.provider}:{spec.model_id})  "
          f"n_test={len(test)}  conditions={conditions}")
    preds = {c: [] for c in conditions}
    calls = {c: 0 for c in conditions}
    errs = {c: 0 for c in conditions}
    for i, ex in enumerate(test):
        for c in conditions:
            tr, err = [], None
            try:
                if c == "baseline":
                    pred, tr = agents.run_baseline(client, spec, task, ex, temperature)
                elif c == "knn":
                    nbrs = knn_neighbors(train, ex, k)
                    pred, tr = agents.run_knn(client, spec, task, ex, nbrs, temperature)
                else:  # tool
                    pred, tr = agents.run_tool(client, spec, task, ex, max_rounds, temperature)
            except Exception as e:  # noqa: BLE001 - keep the sweep going
                pred, err = None, str(e)
            ncalls = sum(1 for t in tr if t.get("role") == "tool")
            preds[c].append(pred)
            calls[c] += ncalls
            errs[c] += int(err is not None)
            ok = pred is not None and pred == ex["gold"]
            if logf:
                logf.write(json.dumps({
                    "i": i, "model": spec.name, "condition": c, "mode": ex["mode"],
                    "template": ex["template"], "gold": ex["gold"], "pred": pred,
                    "correct": ok, "error": err, "n_tool_calls": ncalls,
                    "transcript": tr,
                }) + "\n")
            mark = "OK " if ok else ("ERR" if err else "X  ")
            extra = f" calls={ncalls}" if c == "tool" else ""
            print(f"[{i+1}/{len(test)}] {spec.name:14} {c:8} {mark} "
                  f"pred={pred} gold={ex['gold']}{extra}"
                  + (f"  ({err[:70]})" if err else ""))
    # back-fill None preds with a sentinel so accuracy counts them wrong
    stats = {}
    for c in conditions:
        p = [x if x is not None else "__none__" for x in preds[c]]
        stats[c] = {
            "accuracy": accuracy(test, p),
            "by_mode": by_group(test, p, "mode"),
            "avg_tool_calls": calls[c] / len(test) if test else 0.0,
            "errors": errs[c],
            "n_none": sum(1 for x in preds[c] if x is None),
        }
    return stats


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", default="eval/sample/ambiguous_contracts.jsonl")
    ap.add_argument("--models", default="stub",
                    help="comma list of registry names or provider:model_id")
    ap.add_argument("--condition", default="baseline,tool,knn",
                    help="comma list of {baseline,tool,knn}")
    ap.add_argument("--limit", type=int, default=90, help="evaluated test rows (0 = all)")
    ap.add_argument("--k", type=int, default=5, help="precedents for the knn condition")
    ap.add_argument("--train-frac", type=float, default=0.7, dest="train_frac")
    ap.add_argument("--max-rounds", type=int, default=4, dest="max_rounds")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--out", default="eval/runs/ambiguous_llm.jsonl",
                    help="per-example transcript JSONL")
    ap.add_argument("--results", default="eval/runs/ambiguous_llm_results.json")
    args = ap.parse_args()

    task = data.get_task("ambiguous_contracts")
    rows = load_jsonl(args.data)
    for r in rows:
        r["gold"] = r["answer"]
    train, test_pool = split(rows, args.seed, args.train_frac)
    test = stratified_sample(test_pool, args.limit, args.seed)

    conditions = [c.strip() for c in args.condition.split(",") if c.strip()]
    specs = [models.resolve(m) for m in args.models.split(",") if m.strip()]

    logf = None
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        logf = open(args.out, "w", buffering=1)  # line-buffered: progress is visible live

    print(f"dataset: {len(rows)} rows | precedent pool: {len(train)} | "
          f"test pool: {len(test_pool)} | evaluated: {len(test)}")
    print(f"test label balance: {dict(Counter(r['gold'] for r in test))}")
    print(f"test mode balance: {dict(Counter(r['mode'] for r in test))}")

    table = {}
    for spec in specs:
        try:
            table[spec.name] = run_model(spec, task, test, train, args.k,
                                         args.max_rounds, args.temperature,
                                         conditions, logf)
        except SystemExit as e:   # missing key etc. — skip model, keep sweep
            print(f"  ! skipping {spec.name}: {e}")
    if logf:
        logf.close()

    out = {
        "data": args.data,
        "n_total": len(rows),
        "n_precedent_pool": len(train),
        "n_test": len(test),
        "k": args.k,
        "conditions": conditions,
        "test_label_balance": dict(Counter(r["gold"] for r in test)),
        "test_mode_balance": dict(Counter(r["mode"] for r in test)),
        "results": table,
    }
    os.makedirs(os.path.dirname(args.results) or ".", exist_ok=True)
    with open(args.results, "w") as f:
        json.dump(out, f, indent=2)

    # ── comparison table ──
    print(f"\n=== accuracy (n={len(test)}) ===")
    header = "model".ljust(22) + "".join(c.ljust(18) for c in conditions)
    print(header)
    print("-" * len(header))
    for name, stats in table.items():
        row = name.ljust(22)
        for c in conditions:
            s = stats[c]
            cell = f"{s['accuracy']:.0%}"
            if c == "tool":
                cell += f" ({s['avg_tool_calls']:.1f}c)"
            if s["n_none"]:
                cell += f" !{s['n_none']}"
            row += cell.ljust(18)
        print(row)
    print(f"\nresults -> {args.results}")
    if args.out:
        print(f"transcripts -> {args.out}")


if __name__ == "__main__":
    main()
