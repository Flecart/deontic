"""Experiment A scorer: tables from results.jsonl.

Outputs (markdown to stdout):
  1. verdict accuracy by arm x tier (per model where applicable)
  2. atom-level grounding accuracy by regime x tier (LLM arms), per atom
  3. violation + remedy accuracy on the acted subset
  4. token cost per case by arm

Usage: python score.py --results results.jsonl [--exclude-leaky cases.jsonl]
"""
from __future__ import annotations
import argparse, json
from collections import defaultdict
from pathlib import Path

GROUNDABLE = ["personal_data", "consent", "revoked", "emergency",
              "anonymized", "commercial", "certified"]


def pct(num, den):
    return f"{100*num/den:5.1f}% ({num}/{den})" if den else "    -"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results.jsonl")
    ap.add_argument("--exclude-leaky", default=None,
                    help="cases.jsonl; drop cases with non-empty leak_flags")
    args = ap.parse_args()

    rows = [json.loads(l) for l in Path(args.results).read_text().splitlines() if l]
    if args.exclude_leaky:
        leaky = {json.loads(l)["case_id"] for l in Path(args.exclude_leaky).read_text().splitlines()
                 if l and json.loads(l)["leak_flags"]}
        rows = [r for r in rows if r["case_id"] not in leaky]
        print(f"_(excluded {len(leaky)} leak-flagged cases)_\n")

    # 1. verdict accuracy: arm/model x tier
    acc = defaultdict(lambda: [0, 0])
    for r in rows:
        key = (f"{r['arm']}" + (f"[{r['model']}]" if r["model"] != "-" else ""), r["tier"])
        acc[key][1] += 1
        acc[key][0] += int(r["pred_verdict"]["share_status"] == r["gold"]["share_status"])
    arms = sorted({k[0] for k in acc})
    tiers = sorted({k[1] for k in acc})
    print("## Verdict accuracy (share status) by arm x tier\n")
    print("| arm | " + " | ".join(f"tier {t}" for t in tiers) + " |")
    print("|---|" + "---|" * len(tiers))
    for a in arms:
        cells = [pct(*acc[(a, t)]) if (a, t) in acc else "-" for t in tiers]
        print(f"| {a} | " + " | ".join(cells) + " |")

    # 2. atom-level accuracy by regime x tier (grounding arms only)
    print("\n## Atom-level grounding accuracy (regime x tier)\n")
    aacc = defaultdict(lambda: [0, 0])
    peratom = defaultdict(lambda: [0, 0])
    for r in rows:
        if not r["arm"].startswith(("ground_", "staged_")) or not r["pred_assignment"]:
            continue
        for a in GROUNDABLE:
            ok = int(r["pred_assignment"][a] == r["gold_assignment"][a])
            aacc[(r["arm"], r["model"], r["tier"])][1] += 1
            aacc[(r["arm"], r["model"], r["tier"])][0] += ok
            # per-atom split only on TRUE gold (where tiers differ)
            if r["gold_assignment"][a]:
                peratom[(r["arm"], a, r["tier"])][1] += 1
                peratom[(r["arm"], a, r["tier"])][0] += ok
    if aacc:
        print("| regime[model] | " + " | ".join(f"tier {t}" for t in tiers) + " |")
        print("|---|" + "---|" * len(tiers))
        for (arm, model) in sorted({(k[0], k[1]) for k in aacc}):
            cells = [pct(*aacc[(arm, model, t)]) if (arm, model, t) in aacc else "-"
                     for t in tiers]
            print(f"| {arm}[{model}] | " + " | ".join(cells) + " |")
        print("\n### True-atom recall per atom (regime, tier)\n")
        print("| arm | atom | " + " | ".join(f"tier {t}" for t in tiers) + " |")
        print("|---|---|" + "---|" * len(tiers))
        for (arm, a) in sorted({(k[0], k[1]) for k in peratom}):
            cells = [pct(*peratom[(arm, a, t)]) if (arm, a, t) in peratom else "-"
                     for t in tiers]
            print(f"| {arm} | {a} | " + " | ".join(cells) + " |")

    # 3. violation / remedy on acted subset
    print("\n## Acted subset: violation + remedy detection\n")
    vacc = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        if not r["acted"]:
            continue
        key = f"{r['arm']}" + (f"[{r['model']}]" if r["model"] != "-" else "")
        vacc[key][2] += 1
        vacc[key][0] += int(r["pred_verdict"]["violation"] == r["gold"]["violation"])
        vacc[key][1] += int(r["pred_verdict"]["notify_required"] == r["gold"]["notify_required"])
    print("| arm | violation acc | notify acc | n |")
    print("|---|---|---|---|")
    for k in sorted(vacc):
        v, nt, n = vacc[k]
        print(f"| {k} | {pct(v, n)} | {pct(nt, n)} | {n} |")

    # 3b. paraphrase flip-rate: same (assignment, tier), different narration
    groups = defaultdict(list)
    for r in rows:
        base, tv = r["case_id"].rsplit("_t", 1)   # aNNN, "T_vV"
        tier = tv.split("_v")[0]
        key = (r["arm"], r["model"], base, tier)
        groups[key].append(r["pred_verdict"]["share_status"])
    multi = {k: v for k, v in groups.items() if len(v) >= 2}
    if multi:
        print("\n## Paraphrase flip-rate (lower = more consistent)\n")
        flips = defaultdict(lambda: [0, 0])
        for (arm, model, _b, _t), preds in multi.items():
            key = f"{arm}[{model}]" if model != "-" else arm
            flips[key][1] += 1
            flips[key][0] += int(len(set(preds)) > 1)
        print("| arm | flip-rate | groups |")
        print("|---|---|---|")
        for k in sorted(flips):
            f, n = flips[k]
            print(f"| {k} | {pct(f, n)} | {n} |")

    # 4. cost
    print("\n## Mean tokens per case (LLM arms)\n")
    tok = defaultdict(lambda: [0, 0])
    for r in rows:
        if r["tokens"]:
            key = f"{r['arm']}[{r['model']}]"
            tok[key][0] += r["tokens"]
            tok[key][1] += 1
    print("| arm | mean tokens | n |")
    print("|---|---|---|")
    for k in sorted(tok):
        s, n = tok[k]
        print(f"| {k} | {s//n if n else 0} | {n} |")


if __name__ == "__main__":
    main()
