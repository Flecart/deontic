"""The ambitious arm — which MORAL NUCLEUS sustains a commons of selfish agents?

A minimal GovSim-style commons (pool regenerates x2, per-capita sustainable share,
collapse < 5), 5 purely selfish agents who each probe at GREED x their fair share.
The institution is a moral theory adjudicating the act `over` (over-extraction),
enforced by the `deontic` engine: when over-extraction is FORBIDDEN, the unlawful
surplus is confiscated to the sustainable share.

The moral nuclei (each a tiny DDL theory targeting `over`, with its own
fact-finder lens):

  none        no institution
  legalism    the literal Decalogue: forbids THEFT of an owner's property, but a
              commons has no owner — depleting it victimises no identifiable
              neighbour, so NO commandment is triggered. (no-plaintiff externality)
  love        love thy neighbour as thyself: over-extraction harms one's fellow
              commoners (present and future), so the fact-finder asserts the harm
              and the act is forbidden. A general PRINCIPLE reaches the diffuse
              harm the enumeration misses.
  utilitarian maximise the total long-run catch: over-extraction is forbidden.
  kantian     universalise the maxim "take more than my share" -> the commons is
              destroyed (self-defeating), so it is forbidden.

Finding: the LETTER of the law (legalism) collapses the commons because no
enumerated commandment names the diffuse harm; every GENERATIVE principle (love,
utility, universalisability) reaches it and sustains the commons — the formal
counterpart of "love is the fulfilling of the law" (Rom 13:10) and of the
REPORT's no-plaintiff-externality result (F6).
"""
from __future__ import annotations

import math

from . import engine

CAP, N, REGEN, COLLAPSE, ROUNDS = 100, 5, 2.0, 5, 18
GREED = 1.6   # selfish agents probe for GREED x their fair share

_ATOMS = """
atom over: the agent extracted more than the per-capita sustainable share
atom harmsNeighbor: the act harms one's fellow commoners (present or future)
atom namedSin: the act is theft of an identifiable owner's property
atom depletesTotal: the act lowers the long-run total yield
atom notUniversalizable: the act's maxim, if universalised, destroys the commons
"""

# Each nucleus = (DDL theory, fact-finder lens mapping an over-extraction to facts).
NUCLEI = {
    "legalism": (
        _ATOMS + "d_theft: namedSin =>O ~over\n",
        lambda over: ({"namedSin"} if False else set())),   # commons has no owner: never theft
    "love": (
        _ATOMS + "l_harm: harmsNeighbor =>O ~over\n",
        lambda over: ({"harmsNeighbor"} if over else set())),
    "utilitarian": (
        _ATOMS + "u_total: depletesTotal =>O ~over\n",
        lambda over: ({"depletesTotal"} if over else set())),
    "kantian": (
        _ATOMS + "k_univ: notUniversalizable =>O ~over\n",
        lambda over: ({"notUniversalizable"} if over else set())),
}


def threshold(pool):
    return max(1, int((REGEN - 1) * pool / (N * REGEN)))


def run(mode):
    pool = float(CAP)
    theory, lens = (None, None) if mode == "none" else NUCLEI[mode]
    traj = [round(pool)]
    for _ in range(ROUNDS):
        if pool < COLLAPSE:
            break
        thr = threshold(pool)
        intents = {i: max(1, math.ceil(thr * GREED)) for i in range(N)}
        catches = {}
        for i in range(N):
            over = intents[i] > thr
            if theory is None:
                forbidden = False
            else:
                forbidden = engine.verdict(theory, lens(over), "over") == "forbidden"
            # enforce: confiscate unlawful surplus back to the sustainable share
            catches[i] = thr if (over and forbidden) else intents[i]
        pool = min(CAP, max(0.0, pool - sum(catches.values())) * REGEN)
        traj.append(round(pool))
    survived = len(traj) - 1 >= ROUNDS and pool >= COLLAPSE
    return traj, survived


def main():
    print(f"Commons (N={N}, regen x{REGEN}, greed {GREED}, {ROUNDS} rounds)\n")
    print(f"{'moral nucleus':12s} | sustained | final pool | trajectory")
    print("-" * 70)
    rows = {}
    for mode in ["none", "legalism", "love", "utilitarian", "kantian"]:
        traj, surv = run(mode)
        rows[mode] = {"survived": surv, "final": traj[-1], "trajectory": traj}
        print(f"{mode:12s} |   {str(surv):5s}   |    {traj[-1]:3d}     | {traj}")
    print("\nThe letter (legalism: 'no owner, no theft') collapses the commons;")
    print("every generative principle (love / utility / universalisability) sustains it.")
    import json, os
    runs = os.path.join(os.path.dirname(__file__), "runs")
    os.makedirs(runs, exist_ok=True)
    json.dump(rows, open(os.path.join(runs, "bible_govsim.json"), "w"), indent=2)
    return rows


if __name__ == "__main__":
    main()
