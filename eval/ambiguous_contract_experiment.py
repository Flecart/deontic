#!/usr/bin/env python3
"""With/without-deontic experiment for ambiguous_contracts.jsonl."""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
from collections import Counter, defaultdict

try:
    import agents
    import data
    import models
except ImportError:  # pragma: no cover
    from . import agents, data, models


def load_jsonl(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def surface_baseline(row: dict) -> str:
    """A deliberately non-formal text heuristic.

    It sees modal words in the clause but does not resolve facts, nested
    exceptions, or priority. This approximates a brittle direct-answer baseline.
    """
    text = row["text"].lower()
    mode = row["mode"]
    if mode == "must":
        return "Yes" if re.search(r"\b(shall|must|required to)\b(?!\s+not)", text) else "No"
    if mode == "must_not":
        return "Yes" if re.search(r"\b(shall not|may not|must not|prohibited|not permitted)\b", text) else "No"
    if re.search(r"\b(may|permitted|excepted|does not apply)\b", text):
        return "Yes"
    return "No"


def vector(row: dict) -> set[str]:
    return {f"template={row['template']}", f"mode={row['mode']}", *[f"fact={f}" for f in row["facts"]]}


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a or b else 1.0


def knn_predict(train: list[dict], row: dict, k: int = 5) -> str:
    rv = vector(row)
    scored = sorted(((jaccard(vector(t), rv), t["answer"]) for t in train), reverse=True)
    votes = Counter(ans for _, ans in scored[:k])
    return votes.most_common(1)[0][0]


def accuracy(rows: list[dict], preds: list[str | None]) -> float:
    return sum(p == r["answer"] for p, r in zip(preds, rows)) / len(rows)


def by_group(rows: list[dict], preds: list[str | None], key: str) -> dict[str, float]:
    groups = defaultdict(list)
    for r, p in zip(rows, preds):
        groups[r[key]].append(int(p == r["answer"]))
    return {k: sum(v) / len(v) for k, v in sorted(groups.items())}


def split(rows: list[dict], seed: int, frac: float):
    by_template = defaultdict(list)
    for r in rows:
        by_template[r["template"]].append(r)
    rng = random.Random(seed)
    train, test = [], []
    for group in by_template.values():
        rng.shuffle(group)
        k = max(1, int(round(len(group) * frac)))
        train.extend(group[:k])
        test.extend(group[k:])
    rng.shuffle(train)
    rng.shuffle(test)
    return train, test


def llm_baseline_predict(rows: list[dict], model_name: str, temperature: float,
                         log_path: str | None = None) -> tuple[list[str | None], Counter]:
    """Run the direct no-tool LLM baseline used by eval/run.py on these rows."""
    task = data.get_task("ambiguous_contracts")
    spec = models.resolve(model_name)
    client = models.make_client(spec)
    preds: list[str | None] = []
    stats: Counter = Counter()
    logf = None
    if log_path:
        os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
        logf = open(log_path, "w")
    try:
        for i, row in enumerate(rows):
            ex = dict(row)
            ex["gold"] = data.normalize_answer(task, row["answer"])
            try:
                pred, transcript = agents.run_baseline(client, spec, task, ex, temperature)
                err = None
            except Exception as e:  # noqa: BLE001 - keep a long run from dying
                pred, transcript, err = None, [], str(e)
            preds.append(pred)
            stats["total"] += 1
            stats["correct"] += int(pred == row["answer"])
            stats["errors"] += int(err is not None)
            if logf:
                logf.write(json.dumps({
                    "i": i, "id": row.get("id"), "condition": "llm_baseline",
                    "model": spec.name, "task": task["name"], "hypothesis": ex["hypothesis"],
                    "gold": ex["gold"], "pred": pred, "correct": pred == row["answer"],
                    "error": err, "transcript": transcript,
                }) + "\n")
            mark = "OK " if pred == row["answer"] else ("ERR" if err else "X  ")
            print(f"[{i+1}/{len(rows)}] llm_baseline {mark} pred={pred} gold={row['answer']}"
                  + (f" ({err[:80]})" if err else ""))
    finally:
        if logf:
            logf.close()
    return preds, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="eval/sample/ambiguous_contracts.jsonl")
    ap.add_argument("--out", default="eval/runs/ambiguous_contract_results.json")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--train-frac", type=float, default=0.7)
    ap.add_argument("--baseline-model", default=os.environ.get("AMBIGUOUS_BASELINE_MODEL", "gpt-4o-mini"),
                    help="direct no-tool LLM baseline model, as in eval/run.py")
    ap.add_argument("--baseline-log", default="eval/runs/ambiguous_contract_llm_baseline.jsonl",
                    help="write direct LLM baseline transcripts here; empty disables logging")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--include-surface-diagnostic", action="store_true",
                    help="also report the old text heuristic as a non-baseline diagnostic")
    args = ap.parse_args()

    rows = load_jsonl(args.data)
    train, test = split(rows, args.seed, args.train_frac)
    llm_baseline, llm_stats = llm_baseline_predict(
        test, args.baseline_model, args.temperature, args.baseline_log or None)
    knn = [knn_predict(train, r) for r in test]

    results = {
        "data": args.data,
        "n_total": len(rows),
        "n_train": len(train),
        "n_test": len(test),
        "label_balance": dict(Counter(r["answer"] for r in rows)),
        "llm_baseline_model": args.baseline_model,
        "llm_baseline": dict(llm_stats),
        "accuracy": {
            "llm_baseline_no_deontic": accuracy(test, llm_baseline),
            "knn_precedent_no_deontic": accuracy(test, knn),
        },
        "by_mode": {
            "llm_baseline_no_deontic": by_group(test, llm_baseline, "mode"),
            "knn_precedent_no_deontic": by_group(test, knn, "mode"),
        },
    }
    if args.include_surface_diagnostic:
        surface = [surface_baseline(r) for r in test]
        results["accuracy"]["surface_heuristic_diagnostic"] = accuracy(test, surface)
        results["by_mode"]["surface_heuristic_diagnostic"] = by_group(test, surface, "mode")

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)

    print(f"dataset: {len(rows)} examples ({len(train)} train / {len(test)} test)")
    print(f"labels: {results['label_balance']}")
    print(f"llm baseline model: {args.baseline_model} "
          f"(errors: {llm_stats['errors']}/{llm_stats['total']})")
    print("\naccuracy")
    for name, acc in results["accuracy"].items():
        print(f"  {name:26s} {acc:.1%} ({math.floor(acc * len(test) + 1e-9)}/{len(test)})")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
