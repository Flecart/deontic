#!/usr/bin/env python3
"""Transparent reproduction of every headline number, straight from the logs.

For each statute it reads two files:
  - results_*.jsonl : one row per (case, arm, model). Each row has
        gold_assignment  : the TRUE atoms (engine input; gold by construction)
        pred_assignment  : the atoms an LLM grounded (None for holistic/oracle)
        gold / pred_verdict : the engine's gold verdict and the arm's verdict
  - cases_*.jsonl   : one row per case, carries leak_flags (we exclude any
        case with a non-empty leak_flags from every number below)

Every metric is a plain count/total you can re-derive by hand:
  atom accuracy  = (# atoms where pred==gold) / (# atoms), over all atoms+cases
  true-recall    = on gold-TRUE atoms only: # predicted true / # gold true
  false-positive = on gold-FALSE atoms only: # predicted true / # gold false
  verdict acc    = # cases where pred_verdict.status == gold.status / # cases
Tiers: 0 = instance listed in the closed enumeration; 1 = unlisted near-variant;
2 = world-shift instance outside every closed category ("the e-scooter").

Pooled tables use the three families common to every run (no gpt-5.4).
Run:  python reproduce_results.py            # all statutes + pooled
      python reproduce_results.py --statute A
      python reproduce_results.py --families gpt-4.1            # one family
"""
from __future__ import annotations
import argparse, json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
COMMON_FAMILIES = ["gpt-4.1", "deepseek-v4-flash", "qwen3.6-plus"]  # gpt-5.4 excluded

# statute -> (results file, cases file, verdict key, optional grounding override).
# expD's grounding override uses the within_scope-fixed re-grounding run; its
# holistic/program/oracle still come from the main file (see paper Appendix H).
STATUTES = {
    "A": ("expA/results_stage2_main.jsonl", "expA/cases_stage2_memo.jsonl", "share_status",  None),
    "B": ("expB/results_main.jsonl",        "expB/cases_memo.jsonl",        "draw_status",   None),
    "C": ("expC/results.jsonl",             "expC/cases.jsonl",             "enter_status",  None),
    "D": ("expD/results_main.jsonl",        "expD/cases_memo.jsonl",        "honor_status",  "expD/results_reground.jsonl"),
    "E": ("expE/results_main.jsonl",        "expE/cases_memo.jsonl",        "accept_status", None),
    "F": ("expF/results_main.jsonl",        "expF/cases_memo.jsonl",        "act_status",    None),
}
NAMES = {"A": "transfer", "B": "commons", "C": "park", "D": "agency", "E": "sale", "F": "safety"}
TIERS = (0, 1, 2)


def load(results, cases, override):
    """Return (rows, n_total, n_leaky). Leak-flagged cases are dropped."""
    leaky = {json.loads(l)["case_id"] for l in (HERE / cases).open() if json.loads(l).get("leak_flags")}
    rows = [json.loads(l) for l in (HERE / results).open() if l.strip()]
    if override:                       # swap grounded arms for the re-grounded run
        ov = [json.loads(l) for l in (HERE / override).open() if l.strip()]
        rows = [r for r in rows if not r["arm"].startswith("ground_")] + ov
    rows = [r for r in rows if r["case_id"] not in leaky]
    return rows, len({r["case_id"] for r in rows}), len(leaky)


def atom_acc(rows, arm, fams, tier):
    c = n = 0
    for r in rows:
        if r["arm"] == arm and r.get("model") in fams and r["tier"] == tier and r.get("pred_assignment"):
            for a, g in r["gold_assignment"].items():
                n += 1; c += int(r["pred_assignment"][a] == g)
    return c, n


def recall_fp(rows, arm, fams, tier):
    rc = [0, 0]; fp = [0, 0]
    for r in rows:
        if r["arm"] == arm and r.get("model") in fams and r["tier"] == tier and r.get("pred_assignment"):
            for a, g in r["gold_assignment"].items():
                (rc if g else fp)[1] += 1
                (rc if g else fp)[0] += int(r["pred_assignment"][a])
    return rc, fp


def verdict_acc(rows, arm, vkey, fams, tier):
    c = n = 0
    for r in rows:
        if r["arm"] == arm and r["tier"] == tier and (r.get("model") in fams or r.get("model") == "-"):
            n += 1; c += int(r["pred_verdict"].get(vkey) == r["gold"][vkey])
    return c, n


def pct(cn):
    c, n = cn
    return f"{100*c/n:5.1f}" if n else "  -  "


def line(label, per_tier):
    return f"  {label:22s} " + " ".join(pct(x) for x in per_tier)


def report_statute(key, fams):
    rf, cf, vkey, ov = STATUTES[key]
    rows, ncase, nleak = load(rf, cf, ov)
    print(f"\n{'='*64}\nStatute {key} ({NAMES[key]})  |  {rf}  |  {ncase} cases, {nleak} leak-excluded")
    print(f"{'-'*64}\n  metric (Tier:           0     1     2 )")
    # atom accuracy
    print("  ATOM ACCURACY (all atoms, pred==gold):")
    cl = [atom_acc(rows, "ground_closed", fams, t) for t in TIERS]
    op = [atom_acc(rows, "ground_open", fams, t) for t in TIERS]
    print(line("closed", cl)); print(line("open", op))
    g = (100*op[2][0]/op[2][1] - 100*cl[2][0]/cl[2][1]) if cl[2][1] and op[2][1] else 0
    print(f"    -> Tier-2 open-closed atom gap: {g:+.1f}")
    # recall / false-positive at Tier 2 (the atom->verdict conversion mechanism)
    print("  TIER-2 true-atom recall / false-positive:")
    for arm in ("ground_closed", "ground_open"):
        rc, fp = recall_fp(rows, arm, fams, 2)
        print(f"    {arm.split('_')[1]:8s} recall {pct(rc).strip()}%   false-pos {pct(fp).strip()}%")
    # verdict accuracy
    print("  VERDICT ACCURACY (pred status == gold status):")
    arms = ["program", "ground_closed", "ground_open", "holistic", "oracle"]
    have = {r["arm"] for r in rows}
    vrows = {}
    for arm in arms:
        if arm not in have:
            continue
        vfams = fams if arm not in ("program", "oracle") else {"-"}
        v = [verdict_acc(rows, arm, vkey, vfams, t) for t in TIERS]
        vrows[arm] = v
        print(line(arm, v))
    if "ground_closed" in vrows and "ground_open" in vrows:
        vc, vo = vrows["ground_closed"][2], vrows["ground_open"][2]
        vg = (100*vo[0]/vo[1] - 100*vc[0]/vc[1]) if vc[1] and vo[1] else 0
        print(f"    -> Tier-2 open-closed VERDICT gap: {vg:+.1f}")
    return rows, vkey


def report_pooled(fams):
    print(f"\n{'#'*64}\nPOOLED over all statutes (families: {', '.join(sorted(fams))})\n{'#'*64}")
    poolA = {"ground_closed": [[0, 0] for _ in TIERS], "ground_open": [[0, 0] for _ in TIERS]}
    poolV = defaultdict(lambda: [[0, 0] for _ in TIERS])
    for key in STATUTES:
        rf, cf, vkey, ov = STATUTES[key]
        rows, _, _ = load(rf, cf, ov)
        for arm in ("ground_closed", "ground_open"):
            for i, t in enumerate(TIERS):
                c, n = atom_acc(rows, arm, fams, t)
                poolA[arm][i][0] += c; poolA[arm][i][1] += n
        for arm in ("program", "ground_closed", "ground_open", "holistic", "oracle"):
            vfams = fams if arm not in ("program", "oracle") else {"-"}
            for i, t in enumerate(TIERS):
                c, n = verdict_acc(rows, arm, vkey, vfams, t)
                poolV[arm][i][0] += c; poolV[arm][i][1] += n
    print("  ATOM ACCURACY (pooled):")
    print(line("closed", poolA["ground_closed"])); print(line("open", poolA["ground_open"]))
    g = 100*poolA["ground_open"][2][0]/poolA["ground_open"][2][1] - 100*poolA["ground_closed"][2][0]/poolA["ground_closed"][2][1]
    print(f"    -> Tier-2 pooled open-closed atom gap: {g:+.1f}")
    print("  VERDICT ACCURACY (pooled):")
    for arm in ("program", "ground_closed", "ground_open", "holistic", "oracle"):
        print(line(arm, poolV[arm]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--statute", choices=list(STATUTES), default=None)
    ap.add_argument("--families", default=None, help="comma list; default = 3 common families")
    args = ap.parse_args()
    fams = set(args.families.split(",")) if args.families else set(COMMON_FAMILIES)
    keys = [args.statute] if args.statute else list(STATUTES)
    for k in keys:
        report_statute(k, fams)
    if not args.statute:
        report_pooled(fams)
    print("\n(Every number above is counts/totals from the .jsonl files named per "
          "statute; re-derive by hand from gold_assignment / pred_assignment / "
          "pred_verdict. Atom layer = grounding; verdict layer = engine output.)")


if __name__ == "__main__":
    main()
