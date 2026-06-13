"""Cross-statute aggregate analysis (the paper's headline tables).

Pools the six statutes over the three families common to every run
(gpt-4.1, deepseek-v4-flash, qwen3.6-plus; gpt-5.4 excluded per cost).
Atom-level open vs closed, and verdict-level grounded vs holistic vs program.

Run from eval/:  python aggregate.py
"""
import json
from collections import defaultdict
from pathlib import Path

FAM = ["gpt-4.1", "deepseek-v4-flash", "qwen3.6-plus"]

# statute -> (results_file, cases_file, verdict_key, open_results_override)
STATUTES = {
    "A transfer":  ("expA/results_stage2_main.jsonl", "expA/cases_stage2_memo.jsonl", "share_status", None),
    "B commons":   ("expB/results_main.jsonl",        "expB/cases_memo.jsonl",        "draw_status",  None),
    "C park":      ("expC/results.jsonl",             "expC/cases.jsonl",             "enter_status", None),
    "D agency":    ("expD/results_main.jsonl",        "expD/cases_memo.jsonl",        "honor_status", "expD/results_reground.jsonl"),
    "E sale":      ("expE/results_main.jsonl",        "expE/cases_memo.jsonl",        "accept_status", None),
    "F safety":    ("expF/results_main.jsonl",        "expF/cases_memo.jsonl",        "act_status",   None),
}


def leaky(cases_file):
    return {json.loads(l)["case_id"] for l in open(cases_file) if json.loads(l).get("leak_flags")}


def load(results_file, cases_file, open_override):
    lk = leaky(cases_file)
    rows = [json.loads(l) for l in open(results_file) if l.strip()]
    rows = [r for r in rows if r["case_id"] not in lk]
    if open_override:  # D: use within_scope-fixed grounding for closed+open
        ov = [json.loads(l) for l in open(open_override) if l.strip()]
        ov = [r for r in ov if r["case_id"] not in lk]
        rows = [r for r in rows if not r["arm"].startswith("ground_")] + ov
    return rows


def atom_acc(rows, arm, tier):
    c = n = 0
    for r in rows:
        if r["arm"] != arm or r.get("model") not in FAM or r["tier"] != tier or not r.get("pred_assignment"):
            continue
        for a, g in r["gold_assignment"].items():
            n += 1; c += int(r["pred_assignment"][a] == g)
    return c, n


def verdict_acc(rows, arm, vkey, tier, pooled_models=True):
    c = n = 0
    for r in rows:
        if r["arm"] != arm or r["tier"] != tier:
            continue
        if r.get("model") not in (FAM + ["-"]):
            continue
        n += 1; c += int(r["pred_verdict"].get(vkey) == r["gold"][vkey])
    return c, n


print("# Cross-statute aggregate (3 families: gpt-4.1, deepseek, qwen)\n")

# ---- atom-level open vs closed ----
print("## Atom-level accuracy by regime x tier (per statute + pooled)\n")
print("| statute | closed T0/T1/T2 | open T0/T1/T2 | open-closed gap T2 |")
print("|---|---|---|---|")
pool = {"ground_closed": defaultdict(lambda: [0, 0]), "ground_open": defaultdict(lambda: [0, 0])}
for name, (rf, cf, vk, ov) in STATUTES.items():
    rows = load(rf, cf, ov)
    cl = [atom_acc(rows, "ground_closed", t) for t in (0, 1, 2)]
    op = [atom_acc(rows, "ground_open", t) for t in (0, 1, 2)]
    if cl[0][1] == 0:
        continue
    for t in (0, 1, 2):
        pool["ground_closed"][t][0] += cl[t][0]; pool["ground_closed"][t][1] += cl[t][1]
        pool["ground_open"][t][0] += op[t][0]; pool["ground_open"][t][1] += op[t][1]
    fc = "/".join(f"{100*c/n:.0f}" for c, n in cl)
    fo = "/".join(f"{100*c/n:.0f}" for c, n in op)
    gap = 100*op[2][0]/op[2][1] - 100*cl[2][0]/cl[2][1]
    print(f"| {name} | {fc} | {fo} | {gap:+.1f} |")
clp = [pool["ground_closed"][t] for t in (0, 1, 2)]
opp = [pool["ground_open"][t] for t in (0, 1, 2)]
fc = "/".join(f"{100*c/n:.1f}" for c, n in clp)
fo = "/".join(f"{100*c/n:.1f}" for c, n in opp)
gap = 100*opp[2][0]/opp[2][1] - 100*clp[2][0]/clp[2][1]
print(f"| **POOLED** | **{fc}** | **{fo}** | **{gap:+.1f}** |")

# ---- verdict-level: grounded best vs holistic vs program ----
print("\n## Verdict accuracy by arm x tier (per statute, pooled families)\n")
print("| statute | program | grnd_closed | grnd_open | holistic |")
print("|---|---|---|---|---|")
vpool = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for name, (rf, cf, vk, ov) in STATUTES.items():
    rows = load(rf, cf, ov)
    def v(arm):
        cs = [verdict_acc(rows, arm, vk, t) for t in (0, 1, 2)]
        if cs[0][1] == 0:
            return "-", cs
        return "/".join(f"{100*c/n:.0f}" for c, n in cs), cs
    pr, prc = v("program"); gc, gcc = v("ground_closed"); go, goc = v("ground_open"); ho, hoc = v("holistic")
    for arm, cs in (("program", prc), ("ground_closed", gcc), ("ground_open", goc), ("holistic", hoc)):
        for t in (0, 1, 2):
            vpool[arm][t][0] += cs[t][0]; vpool[arm][t][1] += cs[t][1]
    print(f"| {name} | {pr} | {gc} | {go} | {ho} |")
print("| **POOLED** | " + " | ".join(
    "**" + "/".join(f"{100*vpool[arm][t][0]/vpool[arm][t][1]:.0f}" if vpool[arm][t][1] else "-" for t in (0,1,2)) + "**"
    for arm in ("program", "ground_closed", "ground_open", "holistic")) + " |")


# ── case-clustered bootstrap CIs on the two aggregate headline claims ────────

def bootstrap_aggregate(resamples=2000, seed=0):
    import random
    rng = random.Random(seed)
    # collect per (statute, case_id) atom counts for closed/open at Tier 2,
    # and per (statute, case_id) verdict correctness for grounded/holistic at T2
    atom = defaultdict(lambda: {"ground_closed": [0, 0], "ground_open": [0, 0]})  # cid -> regime -> [c,n]
    ver = defaultdict(lambda: defaultdict(lambda: [0, 0]))  # cid -> arm -> [c,n]
    keys = []
    for name, (rf, cf, vk, ov) in STATUTES.items():
        rows = load(rf, cf, ov)
        seen = set()
        for r in rows:
            if r["tier"] != 2:
                continue
            cid = (name, r["case_id"])
            if r["arm"] in ("ground_closed", "ground_open") and r.get("model") in FAM and r.get("pred_assignment"):
                c = sum(int(r["pred_assignment"][a] == g) for a, g in r["gold_assignment"].items())
                atom[cid][r["arm"]][0] += c; atom[cid][r["arm"]][1] += len(r["gold_assignment"])
            if r["arm"] in ("ground_closed", "ground_open", "holistic") and r.get("model") in FAM:
                ver[cid][r["arm"]][0] += int(r["pred_verdict"].get(vk) == r["gold"][vk]); ver[cid][r["arm"]][1] += 1
            seen.add(cid)
        keys += list(seen)
    keys = sorted(set(keys))

    def gap(sample):
        cc = cn = oc = on = 0
        for cid in sample:
            cc += atom[cid]["ground_closed"][0]; cn += atom[cid]["ground_closed"][1]
            oc += atom[cid]["ground_open"][0];   on += atom[cid]["ground_open"][1]
        return (100*oc/on - 100*cc/cn) if cn and on else 0.0

    def vmargin(sample):  # best grounded - holistic, verdict acc at T2
        g_c = g_n = h_c = h_n = 0
        for cid in sample:
            g_c += ver[cid]["ground_closed"][0]; g_n += ver[cid]["ground_closed"][1]
            h_c += ver[cid]["holistic"][0];      h_n += ver[cid]["holistic"][1]
        return (100*g_c/g_n - 100*h_c/h_n) if g_n and h_n else 0.0

    gaps, margins = [], []
    for _ in range(resamples):
        s = [rng.choice(keys) for _ in keys]
        gaps.append(gap(s)); margins.append(vmargin(s))
    gaps.sort(); margins.sort()
    def ci(v): return v[int(0.025*len(v))], v[int(0.975*len(v))-1]
    print(f"\n## Bootstrap CIs (case-clustered, {resamples} resamples, Tier 2)\n")
    print(f"- pooled open-closed atom gap: {gap(keys):+.1f} [{ci(gaps)[0]:+.1f}, {ci(gaps)[1]:+.1f}]")
    print(f"- pooled grounded_closed - holistic verdict margin: {vmargin(keys):+.1f} [{ci(margins)[0]:+.1f}, {ci(margins)[1]:+.1f}]")


bootstrap_aggregate()
