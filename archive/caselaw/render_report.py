"""Render Phase A/B JSON results into report-ready markdown tables."""
import json
import os
import statistics

D = os.path.join(os.path.dirname(__file__), "runs")


def f(x, nd=2):
    return "—" if x is None else f"{x:.{nd}f}"


def phaseA():
    res = json.load(open(os.path.join(D, "phaseA.json")))
    arms = ("caselaw", "nn1", "nn3", "constitution")
    out = ["#### Held-out test accuracy (mean of seeds), judge noise ε\n",
           "| theory | caselaw | nn1 | nn3 | constitution | caselaw ε=.2 | nn1 ε=.2 | rules |",
           "|---|---|---|---|---|---|---|---|"]
    means = {a: [] for a in arms}
    for t, d in res.items():
        if not isinstance(d, dict) or "caselaw@0.0" not in d:
            continue
        g = lambda a, e, m="test_acc": d.get(f"{a}@{e}", {}).get(m)
        for a in arms:
            if g(a, "0.0") is not None:
                means[a].append(g(a, "0.0"))
        out.append(f"| {t} | {f(g('caselaw','0.0'))} | {f(g('nn1','0.0'))} | {f(g('nn3','0.0'))} | "
                   f"{f(g('constitution','0.0'))} | {f(g('caselaw','0.2'))} | {f(g('nn1','0.2'))} | "
                   f"{f(g('caselaw','0.0','rule_count'),1)} |")
    out.append(f"| **MEAN** | **{f(statistics.mean(means['caselaw']))}** | "
               f"**{f(statistics.mean(means['nn1']))}** | **{f(statistics.mean(means['nn3']))}** | "
               f"**{f(statistics.mean(means['constitution']))}** | | | |")
    # consistency
    out.append("\n#### Internal consistency at ε=0.2 "
               "(caselaw: residual unresolved dilemmas; k-NN: stored self-contradictions)\n")
    out.append("| theory | caselaw | nn1 |")
    out.append("|---|---|---|")
    for t, d in res.items():
        if not isinstance(d, dict) or "caselaw@0.2" not in d:
            continue
        out.append(f"| {t} | {f(d['caselaw@0.2'].get('consistency'),2)} | "
                   f"{f(d['nn1@0.2'].get('consistency'),2)} |")
    # an example convergence curve
    cl = res.get("T03_nested", {}).get("caselaw@0.0", {}).get("curve")
    if cl:
        out.append(f"\nExample convergence (T03 nested, caselaw, full-space acc every 3 rulings): {cl}")
    return "\n".join(out)


def phaseB():
    p = os.path.join(D, "phaseB.json")
    if not os.path.exists(p):
        return "_Phase B pending._"
    blob = json.load(open(p))
    out = [f"Judge model: **{blob['model']}**\n",
           "| theory | judge_acc | evolved-law test_acc | oracle test_acc | rules | api_calls |",
           "|---|---|---|---|---|---|"]
    for t, r in blob["results"].items():
        if "error" in r:
            out.append(f"| {t} | ERROR: {r['error'][:40]} | | | | |")
            continue
        out.append(f"| {t} | {f(r['judge_acc'])} | {f(r['law_test_acc'])} | "
                   f"{f(r['oracle_test_acc'])} | {r['rule_count']} | {r['api_calls']} |")
    return "\n".join(out)


if __name__ == "__main__":
    print("=== PHASE A ===\n" + phaseA())
    print("\n=== PHASE B ===\n" + phaseB())
