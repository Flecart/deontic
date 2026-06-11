"""Phase A.3 — the no-plaintiff externality problem, and the regulator fix.

Common law is *complaint-driven*: a case exists only when someone sues. Concrete
individual harm has a plaintiff; a diffuse/future harm (a classic externality —
e.g. the commons) does not. So purely complaint-driven case law should learn to
forbid concrete harm but UNDER-ENFORCE the diffuse externality — until a
*regulator* (attorney-general) is empowered to bring cases sua sponte.

Latent law: the action is forbidden if it causes concrete harm OR stresses the
shared resource, unless the affected parties consent.
"""
from __future__ import annotations

import itertools
import random
import statistics

from . import engine
from .experiment import _acc
from .institutions import CaseLawInstitution, Judge

LATENT = """
atom act: perform the action
atom harmed: a concrete individual is harmed (has a plaintiff)
atom stressed: the shared resource is stressed (diffuse harm, no plaintiff)
atom consent: the affected parties consented
atom rainy: it was raining (irrelevant)
r1: harmed =>O ~act
r2: stressed =>O ~act
r3: consent ~>O act
superiority: r3 > r1, r3 > r2
"""
FACTS = ["harmed", "stressed", "consent", "rainy"]
DECLS = "\n".join(l for l in LATENT.splitlines() if l.strip().startswith("atom "))


def all_cases():
    out = []
    for r in range(len(FACTS) + 1):
        out += [frozenset(c) for c in itertools.combinations(FACTS, r)]
    return out


def litigated(case, regulator):
    """A case reaches court if it has a plaintiff (harmed) — or, with a regulator,
    also when the resource is stressed."""
    if "harmed" in case:
        return True
    return regulator and "stressed" in case


def run(regulator, seed, repeats=5):
    judge = Judge(LATENT, "act", eps=0.0, seed=seed)
    inst = CaseLawInstitution(DECLS, "act", FACTS)
    cases = all_cases()
    stream = [c for c in cases if litigated(c, regulator)] * repeats
    random.Random(seed).shuffle(stream)
    for c in stream:
        inst.learn(c, judge.rule(c))
    # critical region: diffuse externality with no individual plaintiff
    crit = [c for c in cases if "stressed" in c and "harmed" not in c and "consent" not in c]
    crit_acc = _acc(inst, crit, judge)
    overall = _acc(inst, cases, judge)
    # is the externality actually forbidden by the learned law?
    enforced = statistics.mean(inst.predict(c) == "forbidden" for c in crit)
    return overall, crit_acc, enforced


def main():
    print("regulator | overall_acc | externality_region_acc | externality_enforced_rate")
    for reg in (False, True):
        o = statistics.mean(run(reg, s)[0] for s in range(3))
        c = statistics.mean(run(reg, s)[1] for s in range(3))
        e = statistics.mean(run(reg, s)[2] for s in range(3))
        print(f"   {str(reg):5s}  |   {o:.2f}      |       {c:.2f}           |    {e:.2f}")


if __name__ == "__main__":
    main()
