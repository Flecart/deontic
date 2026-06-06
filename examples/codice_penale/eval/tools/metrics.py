#!/usr/bin/env python3
"""metrics — score results/predictions.jsonl against the dataset gold.

Reports, per arm:
  - verdict accuracy (+ offence-id accuracy on `offence` verdicts)
  - pair-accuracy: fraction of minimal pairs where BOTH twins are correct
    (the headline discrimination metric)
  - per-tier accuracy curve (the scaling curve)
  - grounding accuracy (deontic arm): pred_atoms vs atoms_gold, reported
    separately from the verdict — isolates grounding error from deduction
  - calibrated abstention on unresolved items (did the arm abstain/flag?)
  - cost: mean tokens + latency per item

Usage:  python3 metrics.py [results/predictions.jsonl] [--dataset v0_pilot]
"""
from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = os.path.normpath(os.path.join(HERE, ".."))


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("predictions", nargs="?",
                    default=os.path.join(EVAL, "results", "predictions.jsonl"))
    ap.add_argument("--dataset", default="v0_pilot")
    args = ap.parse_args()

    gold = {it["id"]: it for it in
            load(os.path.join(EVAL, "dataset", f"{args.dataset}.jsonl"))}
    preds = load(args.predictions)

    # index predictions by (arm, id)
    by_arm = defaultdict(dict)
    for p in preds:
        by_arm[p["arm"]][p["id"]] = p

    for arm in sorted(by_arm):
        rows = by_arm[arm]
        n = correct = off_correct = off_total = 0
        tier_tot = defaultdict(int); tier_cor = defaultdict(int)
        ground_atoms = ground_correct = 0
        abst_tot = abst_ok = 0
        toks = lat = 0.0
        for iid, g in gold.items():
            p = rows.get(iid)
            if not p:
                continue
            n += 1
            gv = g["gold"]["verdict"]
            ok = (p["pred_verdict"] == gv)
            correct += ok
            tier_tot[g["tier"]] += 1
            tier_cor[g["tier"]] += ok
            if gv == "offence":
                off_total += 1
                off_correct += (p.get("pred_offence") == g["gold"]["offence"])
            if gv == "unresolved":
                abst_tot += 1
                abst_ok += (p["pred_verdict"] == "unresolved")
            if arm == "deontic" and p.get("pred_atoms"):
                for a, gv01 in g["atoms_gold"].items():
                    ground_atoms += 1
                    ground_correct += (int(p["pred_atoms"].get(a, 0)) == gv01)
            toks += p.get("input_tokens", 0) + p.get("output_tokens", 0)
            lat += p.get("latency_s", 0.0)

        # pair accuracy
        pairs, both_ok = set(), 0
        for iid, g in gold.items():
            twin = g.get("minimal_pair")
            if not twin or (twin, iid) in pairs or iid not in rows:
                continue
            pairs.add((iid, twin))
            pa = rows.get(iid); pb = rows.get(twin)
            ga = g["gold"]["verdict"]; gb = gold[twin]["gold"]["verdict"]
            if pa and pb and pa["pred_verdict"] == ga and pb["pred_verdict"] == gb:
                both_ok += 1

        print(f"\n=== {arm} (n={n}) ===")
        print(f"  verdict accuracy : {correct}/{n} = {correct/n:.0%}" if n else "  (no rows)")
        if off_total:
            print(f"  offence-id acc.  : {off_correct}/{off_total} = {off_correct/off_total:.0%}")
        print(f"  pair-accuracy    : {both_ok}/{len(pairs)} = "
              f"{(both_ok/len(pairs)) if pairs else 0:.0%}  (both twins correct)")
        print("  per-tier         : " + "  ".join(
            f"T{t}={tier_cor[t]}/{tier_tot[t]}" for t in sorted(tier_tot)))
        if arm == "deontic" and ground_atoms:
            print(f"  grounding acc.   : {ground_correct}/{ground_atoms} = "
                  f"{ground_correct/ground_atoms:.0%}  (atom-level)")
        if abst_tot:
            print(f"  abstention       : {abst_ok}/{abst_tot} unresolved flagged")
        if n:
            print(f"  cost             : {toks/n:.0f} tok/item, {lat/n:.2f}s/item")

    print("\nExpect: deontic ≥ rag ≥ llm_only; gap widening T1→T4; "
          "pair-accuracy gap largest.")


if __name__ == "__main__":
    main()
