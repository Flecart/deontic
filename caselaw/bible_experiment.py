"""Gospel case-law experiment.

Compares moral architectures on Jesus's recorded verdicts (bible_dataset):

  FIXED arms (written from a principle, not fitted to labels):
    decalogue  the written law alone (legalism)
    love       love-of-neighbour only
    hybrid     love supreme + Decalogue as overridable default (the Gospel design)
  EVOLVED arm:
    caselaw    a defeasible theory SYNTHESIZED from Jesus's rulings on the train
               split (Jesus as the judge), tested on held-out episodes

Metrics:
  test_acc     held-out verdict fidelity (episode-level split; leakage control)
  full_acc     fidelity over the whole corpus
  coherence    residual [JUDGE] deadlocks across the corpus (lower = better)
  rules        rule count (parsimony; learned arms only)

Plus the SUPREME-PRINCIPLE ABLATION: hybrid vs hybrid-with-no-superiority,
isolating whether love-as-supreme is load-bearing (it should turn the
sabbath/mercy cases into unresolved deadlocks).
"""
from __future__ import annotations

import json
import os
import random
import statistics

from . import engine
from . import bible_theories as T
from .bible_dataset import EPISODES, FACT_ATOMS
from .institutions import CaseLawInstitution, ConstitutionInstitution

NAMES = list(EPISODES.keys())


def gold(name):
    return EPISODES[name]["verdict"]


def split(seed, frac=0.6):
    ns = list(NAMES)
    random.Random(seed * 131 + 7).shuffle(ns)
    k = max(1, int(round(len(ns) * frac)))
    return ns[:k], ns[k:]


def coherence(ddl):
    """Episodes left as an unresolved deontic deadlock under this theory."""
    return sum(engine.has_unresolved_conflict(ddl, EPISODES[n]["facts"], "act")
               for n in NAMES)


def run_fixed(arm, test):
    ddl = T.THEORIES[arm]
    acc = sum(engine.verdict(ddl, EPISODES[n]["facts"], "act") == gold(n)
              for n in test) / len(test)
    full = sum(engine.verdict(ddl, EPISODES[n]["facts"], "act") == gold(n)
               for n in NAMES) / len(NAMES)
    return {"test_acc": acc, "full_acc": full, "coherence": coherence(ddl),
            "rules": ddl.count("=>O") + ddl.count("~>O")}


def run_caselaw(seed, train, test):
    inst = CaseLawInstitution(T.ATOMS, "act", FACT_ATOMS)
    stream = list(train)
    random.Random(seed).shuffle(stream)
    for n in stream:                       # Jesus (the text) supplies each verdict
        inst.learn(frozenset(EPISODES[n]["facts"]), gold(n))
    acc = sum(inst.predict(frozenset(EPISODES[n]["facts"])) == gold(n)
              for n in test) / len(test)
    full = sum(inst.predict(frozenset(EPISODES[n]["facts"])) == gold(n)
               for n in NAMES) / len(NAMES)
    cons = inst.dilemmas([frozenset(EPISODES[n]["facts"]) for n in NAMES])
    return {"test_acc": acc, "full_acc": full, "coherence": cons, "rules": inst.size()}


def ablation():
    """Supreme-principle ablation: hybrid vs hybrid with no superiority."""
    full = T.HYBRID
    abl = T.HYBRID_NO_SUPREME
    out = {}
    for tag, ddl in (("hybrid", full), ("hybrid_no_supreme", abl)):
        acc = sum(engine.verdict(ddl, EPISODES[n]["facts"], "act") == gold(n)
                  for n in NAMES) / len(NAMES)
        deadlocked = [n for n in NAMES
                      if engine.has_unresolved_conflict(ddl, EPISODES[n]["facts"], "act")]
        out[tag] = {"full_acc": acc, "deadlocks": deadlocked}
    return out


def main(seeds=range(8)):
    fixed = ["decalogue", "love", "hybrid"]
    res = {a: {"test": [], "full": None, "coherence": None, "rules": None} for a in fixed}
    res["caselaw"] = {"test": [], "full": [], "coherence": [], "rules": []}
    for s in seeds:
        train, test = split(s)
        for a in fixed:
            r = run_fixed(a, test)
            res[a]["test"].append(r["test_acc"])
            res[a]["full"], res[a]["coherence"], res[a]["rules"] = (
                r["full_acc"], r["coherence"], r["rules"])
        cl = run_caselaw(s, train, test)
        for k, kk in (("test", "test_acc"), ("full", "full_acc"),
                      ("coherence", "coherence"), ("rules", "rules")):
            res["caselaw"][k].append(cl[kk])

    summary = {}
    for a in fixed:
        summary[a] = {"test_acc": round(statistics.mean(res[a]["test"]), 3),
                      "full_acc": round(res[a]["full"], 3),
                      "coherence": res[a]["coherence"], "rules": res[a]["rules"]}
    summary["caselaw"] = {
        "test_acc": round(statistics.mean(res["caselaw"]["test"]), 3),
        "full_acc": round(statistics.mean(res["caselaw"]["full"]), 3),
        "coherence": round(statistics.mean(res["caselaw"]["coherence"]), 2),
        "rules": round(statistics.mean(res["caselaw"]["rules"]), 1)}

    out = {"summary": summary, "ablation": ablation(),
           "n_episodes": len(NAMES), "n_seeds": len(list(seeds))}
    runs = os.path.join(os.path.dirname(__file__), "runs")
    os.makedirs(runs, exist_ok=True)
    json.dump(out, open(os.path.join(runs, "bible.json"), "w"), indent=2)
    return out


def show(out):
    print(f"\nGospel case-law: {out['n_episodes']} episodes, "
          f"{out['n_seeds']} seeds (held-out 40%)\n")
    print(f"{'arm':12s} | held-out | full | coherence(deadlocks) | rules")
    print("-" * 60)
    for a, d in out["summary"].items():
        print(f"{a:12s} |   {d['test_acc']:.2f}   | {d['full_acc']:.2f} |"
              f"         {d['coherence']:<11} | {d['rules']}")
    abl = out["ablation"]
    print("\nSUPREME-PRINCIPLE ABLATION (remove love-grounded superiority):")
    print(f"  hybrid            full_acc={abl['hybrid']['full_acc']:.2f}  "
          f"deadlocks={len(abl['hybrid']['deadlocks'])}")
    print(f"  hybrid_no_supreme full_acc={abl['hybrid_no_supreme']['full_acc']:.2f}  "
          f"deadlocks={len(abl['hybrid_no_supreme']['deadlocks'])} "
          f"-> {abl['hybrid_no_supreme']['deadlocks']}")


if __name__ == "__main__":
    show(main())
