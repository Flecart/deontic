"""E2 scorer: sample-efficiency curves from results_e2.jsonl.

  1. verdict accuracy vs store size n, per policy (pooled over models; the
     E2 deliverable — hypothesis dispute ~ oracle >> uniform)
  2. same per model (spread check)
  3. inter-model agreement (mean pairwise Cohen's kappa) vs n per policy
  4. retrieval P@k vs n per policy
  5. dispute vs dispute_adj at matched n = the adjudicator-noise tax

Usage: python e2_score.py --results runs/e2/results_e2.jsonl
"""
from __future__ import annotations
import argparse, itertools, json
from collections import defaultdict
from pathlib import Path

from e1_score import kappa, pct


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    args = ap.parse_args()
    rows = [json.loads(l) for l in Path(args.results).read_text().splitlines() if l]

    policies = sorted({r["policy"] for r in rows})
    sizes = sorted({r["store_n"] for r in rows})
    models = sorted({r["model"] for r in rows})
    ok = lambda r: r["pred_verdict"]["share_status"] == r["gold"]["share_status"]

    print("## Verdict accuracy vs store size (pooled over models)\n")
    print("| policy | " + " | ".join(f"n={n}" for n in sizes) + " |")
    print("|---|" + "---|" * len(sizes))
    for p in policies:
        cells = []
        for n in sizes:
            sel = [r for r in rows if r["policy"] == p and r["store_n"] == n]
            cells.append(pct(sum(map(ok, sel)), len(sel)))
        print(f"| {p} | " + " | ".join(cells) + " |")

    if len(models) > 1:
        print("\n## Per model\n")
        print("| policy | model | " + " | ".join(f"n={n}" for n in sizes) + " |")
        print("|---|---|" + "---|" * len(sizes))
        for p, m in itertools.product(policies, models):
            cells = []
            for n in sizes:
                sel = [r for r in rows if r["policy"] == p and r["store_n"] == n
                       and r["model"] == m]
                cells.append(pct(sum(map(ok, sel)), len(sel)))
            print(f"| {p} | {m} | " + " | ".join(cells) + " |")

        print("\n## Inter-model agreement (mean pairwise kappa) vs n\n")
        print("| policy | " + " | ".join(f"n={n}" for n in sizes) + " |")
        print("|---|" + "---|" * len(sizes))
        for p in policies:
            cells = []
            for n in sizes:
                preds = defaultdict(dict)
                for r in rows:
                    if r["policy"] == p and r["store_n"] == n:
                        preds[r["case_id"]][r["model"]] = r["pred_verdict"]["share_status"]
                ks = []
                for m1, m2 in itertools.combinations(models, 2):
                    pairs = [(v[m1], v[m2]) for v in preds.values()
                             if m1 in v and m2 in v]
                    if pairs:
                        ks.append(kappa(pairs))
                cells.append(f"{sum(ks)/len(ks):.3f}" if ks else "-")
            print(f"| {p} | " + " | ".join(cells) + " |")

    print("\n## Retrieval P@k vs n (rows with >=1 relevant in store)\n")
    print("| policy | " + " | ".join(f"n={n}" for n in sizes) + " |")
    print("|---|" + "---|" * len(sizes))
    for p in policies:
        cells = []
        for n in sizes:
            sel = [r for r in rows if r["policy"] == p and r["store_n"] == n
                   and r["n_relevant_available"] > 0 and r["retrieved"]]
            if sel:
                pk = sum(r["n_relevant_retrieved"] / len(r["retrieved"])
                         for r in sel) / len(sel)
                cells.append(f"{100*pk:5.1f}%")
            else:
                cells.append("-")
        print(f"| {p} | " + " | ".join(cells) + " |")

    if "dispute" in policies and "dispute_adj" in policies:
        print("\n## Adjudicator-noise tax (dispute gold - dispute_adj, same n)\n")
        print("| n | gold holdings | adjudicated holdings | tax |")
        print("|---|---|---|---|")
        for n in sizes:
            g = [r for r in rows if r["policy"] == "dispute" and r["store_n"] == n]
            a = [r for r in rows if r["policy"] == "dispute_adj" and r["store_n"] == n]
            if g and a:
                ag = sum(map(ok, g)) / len(g)
                aa = sum(map(ok, a)) / len(a)
                print(f"| {n} | {100*ag:5.1f}% | {100*aa:5.1f}% | {100*(ag-aa):+5.1f}pp |")


if __name__ == "__main__":
    main()
