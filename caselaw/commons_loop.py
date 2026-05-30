"""Phase C (lite) — evolved case law governing a dynamic commons.

A minimal GovSim-style commons (pool regenerates x2, cap 100, collapse < 5) with
N selfish agents that each try to over-extract. Three governance modes:
  none     — no institution
  caselaw  — case law evolved FROM AN EMPTY corpus by an oracle judge (over=>forbidden)
  hybrid   — a constitutional floor (over forbidden) present from round 0 + case law

Shows: no institution collapses; evolving-from-empty suffers a COLD-START dip
before the law forms; a constitutional floor prevents the dip. Closes the loop
between the controlled case-law result and the live commons (no LLM needed).
"""
from __future__ import annotations

import math

from .institutions import CaseLawInstitution, HybridCaseLaw, Judge

CAP, N, REGEN, COLLAPSE, ROUNDS = 100, 5, 2.0, 5, 18
GREED = 1.6  # selfish agents try to take GREED x their fair share

# latent commons law (the oracle judge applies it): over-extraction is forbidden.
LATENT = ("atom over: the agent extracted more than the per-capita sustainable share\n"
          "atom prior_offense: the agent over-extracted before (irrelevant to the verdict here)\n"
          "atom stressed: the resource is stressed (irrelevant to the verdict here)\n"
          "r1: =>O ~over\n")
DECLS = "\n".join(l for l in LATENT.splitlines() if l.strip().startswith("atom "))
FACTS = ["over", "prior_offense", "stressed"]


def threshold(pool):
    return max(1, int((REGEN - 1) * pool / (N * REGEN)))


def make_inst(mode):
    if mode == "caselaw":
        return CaseLawInstitution(DECLS, "over", FACTS)
    if mode == "hybrid":     # constitutional floor: a supreme "over is forbidden"
        h = HybridCaseLaw(DECLS, "over", FACTS, supreme=True)
        h.rules = [{"id": "const", "ant": frozenset(), "mod": "F"}]
        h.sup = set(); h._seed_ids = {"const"}
        return h
    return None


def run(mode):
    pool = float(CAP)
    judge = Judge(LATENT, "over", eps=0.0)
    inst = make_inst(mode)
    prior = {i: False for i in range(N)}
    traj = [round(pool)]
    for _ in range(ROUNDS):
        if pool < COLLAPSE:
            break
        thr = threshold(pool)
        intents = {i: max(1, math.ceil(thr * GREED)) for i in range(N)}  # selfish probe
        catches = {}
        for i in range(N):
            over = intents[i] > thr
            facts = set()
            if over: facts.add("over")
            if prior[i]: facts.add("prior_offense")
            if pool < 0.3 * CAP: facts.add("stressed")
            if inst is None:
                verdict = "allowed"
            else:
                # the agent is judged on the act 'over'; the institution learns then rules
                inst.learn(frozenset(facts), judge.rule(frozenset(facts)))
                verdict = inst.predict(frozenset(facts))
            # enforce: if over-extraction is forbidden by the current law, confiscate to share
            catches[i] = thr if (over and verdict == "forbidden") else intents[i]
            prior[i] = catches[i] > thr
        total = sum(catches.values())
        pool = min(CAP, max(0.0, pool - total) * REGEN)
        traj.append(round(pool))
    survived = len(traj) - 1 >= ROUNDS and pool >= COLLAPSE
    return traj, survived


def main():
    print(f"Dynamic commons (N={N}, regen x{REGEN}, greed {GREED}, {ROUNDS} rounds)")
    print("mode     | survived | pool trajectory")
    for mode in ["none", "caselaw", "hybrid"]:
        traj, surv = run(mode)
        print(f"{mode:8s} |   {str(surv):5s}  | {traj}")
    # show the law the case-law mode evolved
    inst = make_inst("caselaw"); judge = Judge(LATENT, "over", eps=0.0)
    for f in [frozenset({"over"}), frozenset()]:
        inst.learn(f, judge.rule(f))
    print("\nLaw evolved by 'caselaw' mode:\n" + inst._theory())


if __name__ == "__main__":
    main()
