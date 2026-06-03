#!/usr/bin/env python3
"""Offline with/without-deontic experiment for ambiguous_contracts.jsonl."""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import subprocess
import tempfile
from collections import Counter, defaultdict

try:
    from ambiguous_contracts import TEMPLATES, answer_for, status_from_template
except ImportError:  # pragma: no cover
    from .ambiguous_contracts import TEMPLATES, answer_for, status_from_template


TEMPLATE_BY_ID = {t.tid: t for t in TEMPLATES}


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


def deontic_binary_status(row: dict, deontic_bin: str) -> str | None:
    if not deontic_bin or not os.path.exists(deontic_bin):
        return None
    body = "facts: " + ", ".join(row["facts"]) + "\n\n" + row["ddl"]
    fd, path = tempfile.mkstemp(suffix=".ddl")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(body)
        proc = subprocess.run([deontic_bin, "query", path, row["target"]],
                              capture_output=True, text=True, timeout=20)
        out = proc.stdout + proc.stderr
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    if "unresolved" in out:
        return "unresolved"
    for line in out.splitlines():
        if re.search(rf"\b{re.escape(row['target'])}\s*:", line):
            rhs = line.split(":", 1)[1].strip()
            if rhs.startswith("O("):
                return "O"
            if rhs.startswith("F("):
                return "F"
            if rhs.startswith(("Ps(", "P(", "Pw(")):
                return "P"
    return "unknown"


def deontic_predict(row: dict, deontic_bin: str | None) -> tuple[str, str]:
    status = deontic_binary_status(row, deontic_bin or "")
    source = "deontic-cli"
    if status is None:
        t = TEMPLATE_BY_ID[row["template"]]
        status = status_from_template(t, set(row["facts"]))
        source = "python-ddl-fallback"
    return answer_for(row["mode"], status), source


def accuracy(rows: list[dict], preds: list[str]) -> float:
    return sum(p == r["answer"] for p, r in zip(preds, rows)) / len(rows)


def by_group(rows: list[dict], preds: list[str], key: str) -> dict[str, float]:
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="eval/sample/ambiguous_contracts.jsonl")
    ap.add_argument("--out", default="eval/runs/ambiguous_contract_results.json")
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--train-frac", type=float, default=0.7)
    ap.add_argument("--deontic-bin", default=os.environ.get("DEONTIC_BIN", ".lake/build/bin/deontic"))
    args = ap.parse_args()

    rows = load_jsonl(args.data)
    train, test = split(rows, args.seed, args.train_frac)
    surface = [surface_baseline(r) for r in test]
    knn = [knn_predict(train, r) for r in test]
    deontic_pairs = [deontic_predict(r, args.deontic_bin) for r in test]
    deontic = [p for p, _ in deontic_pairs]
    source_counts = Counter(src for _, src in deontic_pairs)

    results = {
        "data": args.data,
        "n_total": len(rows),
        "n_train": len(train),
        "n_test": len(test),
        "label_balance": dict(Counter(r["answer"] for r in rows)),
        "deontic_source": dict(source_counts),
        "accuracy": {
            "surface_no_deontic": accuracy(test, surface),
            "knn_precedent_no_deontic": accuracy(test, knn),
            "deontic_system": accuracy(test, deontic),
        },
        "by_mode": {
            "surface_no_deontic": by_group(test, surface, "mode"),
            "knn_precedent_no_deontic": by_group(test, knn, "mode"),
            "deontic_system": by_group(test, deontic, "mode"),
        },
        "by_template_deontic": by_group(test, deontic, "template"),
    }

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(results, f, indent=2)

    print(f"dataset: {len(rows)} examples ({len(train)} train / {len(test)} test)")
    print(f"labels: {results['label_balance']}")
    print(f"deontic source: {dict(source_counts)}")
    print("\naccuracy")
    for name, acc in results["accuracy"].items():
        print(f"  {name:26s} {acc:.1%} ({math.floor(acc * len(test) + 1e-9)}/{len(test)})")
    print(f"\nwrote {args.out}")


if __name__ == "__main__":
    main()
