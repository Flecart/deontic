# The moral constitution of the Gospels — love-supreme, written-law-as-default.
#
# Architecture (the central design claim of this study):
#   * The two great commandments (love God, love neighbour) are the SUPREME
#     invariant — "on these two hang all the law and the prophets" (Matt 22:40).
#   * The written Decalogue duties are DEFEASIBLE DEFAULTS, not an inviolable floor.
#     "I am not come to destroy the law ... but to fulfil it" (Matt 5:17): the law
#     stands, yet love re-orders it where they clash ("the sabbath was made for
#     man, not man for the sabbath", Mark 2:27; "I will have mercy and not
#     sacrifice", Matt 9:13).
#   * Every superiority below is therefore not a brute preference but a *ratio
#     decidendi*: it is grounded, in its comment, in the supreme principle. This
#     is the auditability discipline — a verdict can be traced back to the
#     commandment that licensed it.
#
# This file is the HYBRID (love-supreme + defeasible Decalogue) arm. Its sibling
# `legalism.ddl` drops the love-grounded superiority — the Pharisaic reading —
# and deadlocks or forbids the merciful act. The worked example below is the
# Sabbath healing (Mark 3:1-6); swap the facts to exercise other episodes.

facts: {{FILLED_BY_FACT_FINDER}}

# ── The contested act of the worked example ──────────────────────────────────
atom heal: you do good to relieve a suffering neighbour, here by healing | quote: Is it lawful to do good on the sabbath days ... to save life | uri: sources/gospels.md#L40-L42

# ── Situation atoms (a fact-finder decides these) ────────────────────────────
atom sabbath: it is the sabbath day, on which the law commands rest from work | quote: the sabbath was made for man | uri: sources/gospels.md#L20-L20
atom neighborInNeed: a neighbour is in need or suffering and you are able to relieve it | quote: love thy neighbour as thyself | uri: sources/gospels.md#L8-L8

# ── Supreme principle: love of neighbour / mercy (the floor) ─────────────────
# Love-neighbour generates a positive duty to relieve a neighbour's suffering.
# This is the rule the supremacy ultimately rests on.
mercy: neighborInNeed =>O heal

# ── Written law: keeping the sabbath holy (a defeasible default) ─────────────
# The ritual reading forbids work — and healing is work — on the sabbath.
keepSabbath: sabbath =>O ~heal

# ── The ratio: love re-orders the law ────────────────────────────────────────
# Without this line the two rules deadlock and the engine prints [JUDGE]; the
# legalism.ddl arm leaves exactly that gap. Here the supreme commandment resolves
# it: mercy to the neighbour outranks the ritual of rest.
# ratio: love thy neighbour (Matt 22:39) + "the sabbath was made for man" (Mark
#        2:27) + "I will have mercy and not sacrifice" (Matt 9:13)  ⟹  mercy > keepSabbath
superiority: mercy > keepSabbath
