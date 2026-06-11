"""Phase A — controlled case-law experiment (no LLM).

For each latent theory, present a stream of judged cases and track how each
institution's accumulated law converges to the latent ground truth, stays
internally consistent, and resists judge noise.

Arms:
  caselaw      — incrementally-synthesized defeasible DDL theory (engine-evaluated)
  nn1 / nn3    — k-NN over precedent fact-vectors (no formal structure)
  constitution — a fixed general constitution (never adapts)

Metrics (accuracy measured EXACTLY over the full enumerated case space):
  final_acc, auc (mean acc over the stream), cases_to_95, rule_count,
  consistency (caselaw: residual dilemmas; nn: self-contradictions).
"""
from __future__ import annotations

import itertools
import json
import os
import random
import statistics

from . import engine, theories
from .constitution import CONSTITUTION
from .institutions import (CaseLawInstitution, ConstitutionInstitution, Judge,
                           NearestNeighborInstitution)


def atom_decls(ddl):
    return "\n".join(l for l in ddl.splitlines() if l.strip().startswith("atom "))


def all_cases(facts):
    out = []
    for r in range(len(facts) + 1):
        out += [frozenset(c) for c in itertools.combinations(facts, r)]
    return out


def _acc(inst, cases, judge):
    if not cases:
        return 1.0
    return sum(inst.predict(c) == judge.truth(c) for c in cases) / len(cases)


def split(cases, seed, frac=0.6):
    cs = list(cases)
    random.Random(seed * 97 + 7).shuffle(cs)
    k = max(1, int(round(len(cs) * frac)))
    return cs[:k], cs[k:]


def run_arm(arm, T, eps, seed, repeats=4):
    facts, tgt, ddl = T["facts"], T["target"], T["ddl"]
    cases = all_cases(facts)
    judge = Judge(ddl, tgt, eps=eps, seed=seed)
    decls = atom_decls(ddl)
    train, test = split(cases, seed)
    if arm == "caselaw":
        inst = CaseLawInstitution(decls, tgt, facts)
    elif arm == "hybrid_default":
        from .institutions import HybridCaseLaw
        inst = HybridCaseLaw(decls, tgt, facts, supreme=False)
    elif arm == "hybrid_supreme":
        from .institutions import HybridCaseLaw
        inst = HybridCaseLaw(decls, tgt, facts, supreme=True)
    elif arm == "nn1":
        inst = NearestNeighborInstitution(decls, tgt, facts, k=1)
    elif arm == "nn3":
        inst = NearestNeighborInstitution(decls, tgt, facts, k=3)
    elif arm == "constitution":
        inst = ConstitutionInstitution(CONSTITUTION, tgt)
        return {"test_acc": _acc(inst, test, judge), "full_acc": _acc(inst, cases, judge),
                "curve": [], "rule_count": None, "consistency": 0}
    else:
        raise ValueError(arm)

    rng = random.Random(seed)
    stream = train * repeats
    rng.shuffle(stream)
    curve = []
    for i, c in enumerate(stream, 1):
        inst.learn(c, judge.rule(c))
        if i % 3 == 0 or i == len(stream):
            curve.append(round(_acc(inst, cases, judge), 3))   # full-space convergence
    if arm in ("caselaw", "hybrid_default", "hybrid_supreme"):
        cons = max(inst.dilemmas(cases) - sum(judge.truth(c) == "dilemma" for c in cases), 0)
        rc = inst.size()
    else:
        cons = inst.self_contradictions()
        rc = len(inst.memory)
    return {"test_acc": _acc(inst, test, judge), "full_acc": _acc(inst, cases, judge),
            "curve": curve, "rule_count": rc, "consistency": cons}


def main(seeds=range(3), epses=(0.0, 0.1, 0.2)):
    arms = ["caselaw", "nn1", "nn3", "constitution"]
    results = {}
    for tname, T in theories.THEORIES.items():
        results[tname] = {"structure": T["structure"]}
        for eps in epses:
            for arm in arms:
                runs = [run_arm(arm, T, eps, s) for s in seeds]
                agg = {k: statistics.mean([r[k] for r in runs])
                       for k in ("test_acc", "full_acc", "consistency")
                       if runs[0][k] is not None}
                agg["rule_count"] = (statistics.mean([r["rule_count"] for r in runs])
                                     if runs[0]["rule_count"] is not None else None)
                agg["curve"] = runs[0]["curve"]
                results[tname][f"{arm}@{eps}"] = agg
        print(f"done {tname}", flush=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), "runs"), exist_ok=True)
    out = os.path.join(os.path.dirname(__file__), "runs", "phaseA.json")
    json.dump(results, open(out, "w"), indent=2)
    return results, out


def summary(res):
    print(f"\n{'theory':16s}| HELD-OUT test_acc  eps=0           | eps=0.2          ")
    print(f"{'':16s}| caselaw nn1  nn3  const | caselaw nn1 ")
    agg = {a: [] for a in ("caselaw", "nn1", "nn3", "constitution")}
    for t, d in res.items():
        z = {a: d[f'{a}@0.0']['test_acc'] for a in agg}
        n = {a: d[f'{a}@0.2']['test_acc'] for a in ('caselaw', 'nn1')}
        for a in agg:
            agg[a].append(z[a])
        print(f"{t:16s}|  {z['caselaw']:.2f}   {z['nn1']:.2f} {z['nn3']:.2f} {z['constitution']:.2f} |"
              f"  {n['caselaw']:.2f}   {n['nn1']:.2f}")
    print(f"{'MEAN':16s}|  " + "  ".join(f"{statistics.mean(agg[a]):.2f}"
          for a in ('caselaw', 'nn1', 'nn3', 'constitution')))


if __name__ == "__main__":
    res, out = main()
    summary(res)
    print("\nwrote", out)
