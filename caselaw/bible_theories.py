"""The moral-theory arms for the Gospel case-law study.

Every episode is normalised to a judgment on a single shared target atom `act`
("is *this* contemplated act forbidden / obligatory / permitted, given the
situation?"), so the existing `engine.verdict` + `institutions` machinery applies
unchanged. Situation features (love-relevant facts, written-law triggers, and a
couple of moral distractors) are the fact atoms.

Three FIXED theories embody the architectures we compare. Crucially they are
written from their *principle*, NOT fitted to the per-episode labels — fidelity
is then an honest out-of-sample measurement (see bible_experiment.py):

  DECALOGUE  the written law alone: a list of prohibitions (both tables) + sabbath
             rest. No positive love-duty, no override. ("legalism")
  LOVE       love-of-NEIGHBOUR only (the second great commandment): relieve need,
             do no harm, forgive. Silent on the vertical (love-of-God) axis.
             ("morality reduced to interpersonal niceness")
  HYBRID     the Gospel architecture: love (both commandments) SUPREME, the
             Decalogue kept as an overridable default. "I came not to destroy the
             law but to fulfil it" (Matt 5:17); "the sabbath was made for man"
             (Mark 2:27) supplies the superiority that lets mercy outrank rest.
"""
from __future__ import annotations

# Mandatory grounded atom dictionary, shared by every arm so each theory loads
# against any case. Descriptions are truth-conditions a fact-finder applies.
ATOMS = """
atom act: the contemplated act whose moral status is in question
atom relievesNeed: the act relieves a neighbour's serious need or suffering
atom harmsNeighbor: the act wrongs or harms a neighbour
atom ownNeed: the act meets the actor's own legitimate bodily need (e.g. hunger)
atom forgiveWrong: the act forgives or shows mercy to one who wronged the actor
atom namedSin: the act is one the Decalogue's second table names (murder, adultery, theft, false witness, dishonouring parents)
atom firstTableSin: the act violates the first table (idolatry, blasphemy)
atom breaksSabbath: the act is work performed on the sabbath day
atom dueToGod: the act renders God his due (worship, reverence, what is God's)
atom civilDue: the act discharges a legitimate civil obligation (e.g. lawful tribute)
atom minorNeed: the act relieves only a minor need (an animal, property)
atom selfishGain: the act is for the actor's selfish material gain
atom ownCostly: the act gives away the actor's own goods beyond what duty strictly requires
atom crowdPresent: a crowd was present (morally irrelevant)
atom daytime: it happened during daytime (morally irrelevant)
"""

# ── DECALOGUE: the written law, prohibitions only, no override ────────────────
DECALOGUE = ATOMS + """
d_named:  namedSin      =>O ~act
d_first:  firstTableSin =>O ~act
d_sabb:   breaksSabbath =>O ~act
"""

# ── LOVE (of neighbour only): horizontal ethics, silent on love-of-God ────────
LOVE = ATOMS + """
l_relieve: relievesNeed  =>O act
l_harm:    harmsNeighbor =>O ~act
l_forgive: forgiveWrong  =>O act
l_own:     ownNeed       ~>O act
"""

# ── HYBRID: love supreme + Decalogue as an overridable default ────────────────
# Adds the love-of-God duty (g_due) the neighbour-only arm lacks, and the
# superiority that lets mercy/need defeat the sabbath default. Each `>` is a
# ratio decidendi, grounded in the supreme commandment (audit trail in comments).
HYBRID = ATOMS + """
# written-law defaults (from DECALOGUE)
d_named:  namedSin      =>O ~act
d_first:  firstTableSin =>O ~act
d_sabb:   breaksSabbath =>O ~act
# love of neighbour
l_relieve: relievesNeed  =>O act
l_harm:    harmsNeighbor =>O ~act
l_forgive: forgiveWrong  =>O act
l_own:     ownNeed       ~>O act
# love of God (the first commandment — the neighbour-only arm misses this)
g_due:     dueToGod      =>O act
# ratio: love thy neighbour (Matt 22:39) + "sabbath made for man" (Mark 2:27)
#        ⟹ mercy and need outrank the ritual of rest.
superiority: l_relieve > d_sabb, l_own > d_sabb
"""

THEORIES = {"decalogue": DECALOGUE, "love": LOVE, "hybrid": HYBRID}

# HYBRID with the love-grounded superiority REMOVED — the ablation that isolates
# whether the supreme principle is load-bearing (it should collapse the sabbath
# mercy-cases into [JUDGE] deadlocks). Same rules, no `superiority:` line.
HYBRID_NO_SUPREME = "\n".join(
    l for l in HYBRID.splitlines() if not l.strip().startswith("superiority:")
) + "\n"
