"""Case-clustered bootstrap CIs for the Tier-2 open-closed atom-accuracy gap.

Mirrors the expA Stage-2 confirmatory analysis: resample CASES (clusters) with
replacement, recompute per-resample atom-level accuracy for ground_open and
ground_closed at Tier 2, and report the gap's percentile 95% CI
(2,000 resamples).

Usage: python bootstrap_ci.py --results results_main.jsonl --cases cases_memo.jsonl
"""
from __future__ import annotations
import argparse, json, random
from collections import defaultdict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--cases", default=None, help="exclude leak-flagged cases")
    ap.add_argument("--tier", type=int, default=2)
    ap.add_argument("--resamples", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    leaky = set()
    if args.cases:
        leaky = {json.loads(l)["case_id"] for l in Path(args.cases).read_text().splitlines()
                 if l and json.loads(l)["leak_flags"]}

    # model -> case_id -> {regime: (correct, total)} atom counts
    table = defaultdict(lambda: defaultdict(dict))
    for line in Path(args.results).read_text().splitlines():
        if not line:
            continue
        r = json.loads(line)
        if (r["tier"] != args.tier or r["case_id"] in leaky
                or r["arm"] not in ("ground_open", "ground_closed")
                or not r.get("pred_assignment")):
            continue
        c = sum(int(r["pred_assignment"].get(a) == gv)
                for a, gv in r["gold_assignment"].items())
        n = len(r["gold_assignment"])
        table[r["model"]][r["case_id"]][r["arm"]] = (c, n)

    rng = random.Random(args.seed)
    print(f"Tier-{args.tier} open-closed atom-accuracy gap, "
          f"{args.resamples}-resample case-clustered bootstrap 95% CI\n")
    print("| grounder | closed | open | gap [95% CI] |")
    print("|---|---|---|---|")
    for m in sorted(table):
        cids = [cid for cid, d in table[m].items()
                if "ground_open" in d and "ground_closed" in d]
        def acc(sample, regime):
            c = sum(table[m][cid][regime][0] for cid in sample)
            n = sum(table[m][cid][regime][1] for cid in sample)
            return 100.0 * c / n
        point_c, point_o = acc(cids, "ground_closed"), acc(cids, "ground_open")
        gaps = []
        for _ in range(args.resamples):
            s = [rng.choice(cids) for _ in cids]
            gaps.append(acc(s, "ground_open") - acc(s, "ground_closed"))
        gaps.sort()
        lo, hi = gaps[int(0.025 * len(gaps))], gaps[int(0.975 * len(gaps)) - 1]
        print(f"| {m} | {point_c:.1f} | {point_o:.1f} | "
              f"{point_o-point_c:+.1f} [{lo:+.1f}, {hi:+.1f}] |")


if __name__ == "__main__":
    main()
