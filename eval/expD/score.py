"""Experiment D scorer: agency statute (per-bearer gold).

Like expA/expB plus a sub-agent dimension: the honor verdict (@Principal) and,
separately, sub-agent conduct-duty breach detection (@SubAgent, rules r9/r10).
The verdict space is effectively binary (permitted-to-refuse is ~1 world, a
structural property of agency law), so the honor table carries the
majority-class baseline.

Usage: python score.py --results results.jsonl [--exclude-leaky cases.jsonl]
"""
from __future__ import annotations
import argparse, json
from collections import defaultdict
from pathlib import Path

GROUNDABLE = ["within_scope", "mandate_revoked", "revocation_published",
              "authority_manifested", "counterparty_good_faith", "ratified",
              "self_dealing", "urgent_necessity"]


def pct(num, den):
    return f"{100*num/den:5.1f}% ({num}/{den})" if den else "    -"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results.jsonl")
    ap.add_argument("--exclude-leaky", default=None)
    args = ap.parse_args()

    rows = [json.loads(l) for l in Path(args.results).read_text().splitlines() if l]
    if args.exclude_leaky:
        leaky = {json.loads(l)["case_id"] for l in Path(args.exclude_leaky).read_text().splitlines()
                 if l and json.loads(l)["leak_flags"]}
        rows = [r for r in rows if r["case_id"] not in leaky]
        print(f"_(excluded {len(leaky)} leak-flagged cases)_\n")

    tiers = sorted({r["tier"] for r in rows})

    # majority-class baseline per tier (honor)
    base = defaultdict(lambda: defaultdict(int))
    for r in rows:
        if r["arm"] == "oracle":
            base[r["tier"]][r["gold"]["honor_status"]] += 1
    print("## Honor-verdict accuracy by arm x tier\n")
    print("_majority-class baseline: " + ", ".join(
        f"t{t} {max(base[t].values())/sum(base[t].values())*100:.1f}%" for t in tiers) + "_\n")
    acc = defaultdict(lambda: [0, 0])
    for r in rows:
        key = (f"{r['arm']}" + (f"[{r['model']}]" if r["model"] != "-" else ""), r["tier"])
        acc[key][1] += 1
        acc[key][0] += int(r["pred_verdict"]["honor_status"] == r["gold"]["honor_status"])
    arms = sorted({k[0] for k in acc})
    print("| arm | " + " | ".join(f"tier {t}" for t in tiers) + " |")
    print("|---|" + "---|" * len(tiers))
    for a in arms:
        print(f"| {a} | " + " | ".join(
            pct(*acc[(a, t)]) if (a, t) in acc else "-" for t in tiers) + " |")

    # atom-level accuracy + per-atom recall
    print("\n## Atom-level grounding accuracy (regime x tier)\n")
    aacc = defaultdict(lambda: [0, 0]); peratom = defaultdict(lambda: [0, 0])
    for r in rows:
        if not r["arm"].startswith("ground_") or not r["pred_assignment"]:
            continue
        for a in GROUNDABLE:
            ok = int(r["pred_assignment"][a] == r["gold_assignment"][a])
            aacc[(r["arm"], r["model"], r["tier"])][0] += ok
            aacc[(r["arm"], r["model"], r["tier"])][1] += 1
            if r["gold_assignment"][a]:
                peratom[(r["arm"], a, r["tier"])][0] += ok
                peratom[(r["arm"], a, r["tier"])][1] += 1
    if aacc:
        print("| regime[model] | " + " | ".join(f"tier {t}" for t in tiers) + " |")
        print("|---|" + "---|" * len(tiers))
        for (arm, model) in sorted({(k[0], k[1]) for k in aacc}):
            print(f"| {arm}[{model}] | " + " | ".join(
                pct(*aacc[(arm, model, t)]) if (arm, model, t) in aacc else "-"
                for t in tiers) + " |")
        print("\n### True-atom recall per atom (regime, tier)\n")
        print("| arm | atom | " + " | ".join(f"tier {t}" for t in tiers) + " |")
        print("|---|---|" + "---|" * len(tiers))
        for (arm, a) in sorted({(k[0], k[1]) for k in peratom}):
            print(f"| {arm} | {a} | " + " | ".join(
                pct(*peratom[(arm, a, t)]) if (arm, a, t) in peratom else "-"
                for t in tiers) + " |")

    # acted subset: principal refusal-notice duty
    print("\n## Acted subset (company already refused): violation + notice duty\n")
    vacc = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        if not r["acted"]:
            continue
        key = f"{r['arm']}" + (f"[{r['model']}]" if r["model"] != "-" else "")
        vacc[key][2] += 1
        vacc[key][0] += int(r["pred_verdict"].get("principal_violation") == r["gold"]["principal_violation"])
        vacc[key][1] += int(r["pred_verdict"].get("notify_required") == r["gold"]["notify_required"])
    print("| arm | wrongful-refusal acc | notice-duty acc | n |")
    print("|---|---|---|---|")
    for k in sorted(vacc):
        v, nt, n = vacc[k]
        print(f"| {k} | {pct(v, n)} | {pct(nt, n)} | {n} |")

    # sub-agent conduct-duty breach (engine-mediated arms only: gold is
    # computed from grounded atoms, so holistic has no subagent_breach signal)
    print("\n## Sub-agent conduct-duty breach detection (engine-mediated arms)\n")
    sacc = defaultdict(lambda: [0, 0])
    for r in rows:
        if r["pred_verdict"].get("subagent_breach") is None or r["arm"] in ("holistic", "holistic_closed"):
            continue
        key = f"{r['arm']}" + (f"[{r['model']}]" if r["model"] != "-" else "")
        sacc[key][1] += 1
        sacc[key][0] += int(r["pred_verdict"]["subagent_breach"] == r["gold"]["subagent_breach"])
    print("| arm | breach acc | n |")
    print("|---|---|---|")
    for k in sorted(sacc):
        print(f"| {k} | {pct(*sacc[k])} | {sacc[k][1]} |")

    # paraphrase flip-rate (honor verdict)
    groups = defaultdict(list)
    for r in rows:
        base_id, tv = r["case_id"].rsplit("_t", 1)
        tier = tv.split("_v")[0]
        groups[(r["arm"], r["model"], base_id, tier)].append(r["pred_verdict"]["honor_status"])
    multi = {k: v for k, v in groups.items() if len(v) >= 2}
    if multi:
        print("\n## Paraphrase flip-rate (honor verdict)\n")
        flips = defaultdict(lambda: [0, 0])
        for (arm, model, _b, _t), preds in multi.items():
            key = f"{arm}[{model}]" if model != "-" else arm
            flips[key][1] += 1
            flips[key][0] += int(len(set(preds)) > 1)
        print("| arm | flip-rate | groups |")
        print("|---|---|---|")
        for k in sorted(flips):
            print(f"| {k} | {pct(*flips[k])} | {flips[k][1]} |")


if __name__ == "__main__":
    main()
