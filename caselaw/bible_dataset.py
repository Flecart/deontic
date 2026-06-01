"""The Gospel case corpus: Jesus's recorded verdicts as labelled cases.

Each episode = (facts, verdict, ratio, cite) on the shared target `act`. The
VERDICT is the label and is largely uncontested (the text says what he did/taught);
the RATIO (why) is the interpretive layer we make auditable but do not score as
truth. Features are a faithful reading of the morally-salient facts, assigned
WITHOUT reference to which arm gets the case right.

verdict ∈ {forbidden, obligatory, allowed}.  Feature vectors are unique across
episodes (no identical situation with two verdicts), so the law is well-defined.

Each episode also names which arm(s) it is designed to discriminate, as a comment
in `ratio` — but the scoring is blind to that.
"""
from __future__ import annotations

# name -> dict(facts, verdict, ratio, cite)
EPISODES = {
    # ── divergence: love right where the literal/ritual law is wrong ──────────
    "SabbathHeal": dict(
        facts={"relievesNeed", "breaksSabbath", "crowdPresent"}, verdict="obligatory",
        ratio="do good / save life on the sabbath — mercy outranks rest",
        cite="Mark 3:1-6"),
    "PluckGrain": dict(
        facts={"ownNeed", "breaksSabbath", "daytime"}, verdict="allowed",
        ratio="the hungry may eat on the sabbath — the sabbath was made for man",
        cite="Mark 2:23-28"),
    "GoodSamaritan": dict(
        facts={"relievesNeed"}, verdict="obligatory",
        ratio="love thy neighbour — go and do likewise",
        cite="Luke 10:25-37"),
    "SheepGoats": dict(
        facts={"relievesNeed", "crowdPresent"}, verdict="obligatory",
        ratio="inasmuch as ye did it to the least — feeding the hungry is owed",
        cite="Matt 25:31-46"),
    "HealLeper": dict(
        facts={"relievesNeed", "daytime"}, verdict="obligatory",
        ratio="compassion touches the unclean — mercy over purity",
        cite="Mark 1:40-42"),
    "ForgiveDebtor": dict(
        facts={"forgiveWrong"}, verdict="obligatory",
        ratio="forgive seventy times seven",
        cite="Matt 18:21-35"),
    "DivorceForbidden": dict(
        facts={"harmsNeighbor", "daytime"}, verdict="forbidden",
        ratio="what God joined let no man put asunder — stricter than Moses' writ",
        cite="Mark 10:2-12"),

    # ── mercy vs the penalty of the law ───────────────────────────────────────
    "StoneAdulteress": dict(
        facts={"harmsNeighbor", "crowdPresent"}, verdict="forbidden",
        ratio="he that is without sin — mercy halts the judicial penalty",
        cite="John 8:3-11"),

    # ── agreement: both forbid (control against pro-act bias) ─────────────────
    "Murder": dict(facts={"harmsNeighbor", "namedSin"}, verdict="forbidden",
                   ratio="thou shalt not kill", cite="Matt 19:18"),
    "Adultery": dict(facts={"harmsNeighbor", "namedSin", "crowdPresent"}, verdict="forbidden",
                     ratio="thou shalt not commit adultery", cite="Matt 19:18"),
    "Theft": dict(facts={"harmsNeighbor", "namedSin", "selfishGain"}, verdict="forbidden",
                  ratio="thou shalt not steal", cite="Matt 19:18"),
    "FalseWitness": dict(facts={"harmsNeighbor", "namedSin", "daytime"}, verdict="forbidden",
                         ratio="thou shalt not bear false witness", cite="Matt 19:18"),
    "ZacchaeusFraud": dict(facts={"harmsNeighbor", "namedSin", "selfishGain", "crowdPresent"},
                           verdict="forbidden", ratio="defrauding by false accusation is theft",
                           cite="Luke 19:8"),
    "WithholdCorban": dict(facts={"harmsNeighbor", "namedSin"}, verdict="forbidden",
                           ratio="honour thy father — tradition cannot void the commandment",
                           cite="Mark 7:9-13"),

    # ── love-intensification: Jesus STRICTER than the literal law ─────────────
    "Retaliate": dict(facts={"harmsNeighbor"}, verdict="forbidden",
                      ratio="turn the other cheek — not eye-for-eye", cite="Matt 5:38-39"),
    "AngerContempt": dict(facts={"harmsNeighbor", "crowdPresent"}, verdict="forbidden",
                          ratio="whoso is angry / says 'thou fool' is liable", cite="Matt 5:21-22"),
    "LustfulIntent": dict(facts={"harmsNeighbor", "daytime"}, verdict="forbidden",
                          ratio="looketh to lust hath committed adultery in his heart",
                          cite="Matt 5:27-28"),

    # ── love-of-God / first table: neighbour-only love MISSES these ───────────
    "Idolatry": dict(facts={"firstTableSin"}, verdict="forbidden",
                     ratio="worship the Lord thy God and him only serve", cite="Matt 4:10"),
    "Blasphemy": dict(facts={"firstTableSin", "crowdPresent"}, verdict="forbidden",
                      ratio="hallowed be thy name", cite="Matt 6:9"),
    "WorshipGod": dict(facts={"dueToGod"}, verdict="obligatory",
                       ratio="render to God the things that are God's", cite="Mark 12:17"),

    # ── written rule needed; love-neighbour underdetermines ───────────────────
    "RenderCaesar": dict(facts={"civilDue", "crowdPresent"}, verdict="allowed",
                         ratio="render unto Caesar — lawful to pay tribute", cite="Mark 12:13-17"),
    "EatWithSinners": dict(facts={"crowdPresent", "daytime"}, verdict="allowed",
                           ratio="they that be whole need not a physician — fellowship permitted",
                           cite="Matt 9:10-13"),

    # ── love-of-neighbour OVER-permits; the sabbath default must stand ────────
    "SabbathProfit": dict(facts={"breaksSabbath", "selfishGain"}, verdict="forbidden",
                          ratio="ordinary gainful work on the sabbath is still forbidden — "
                                "only mercy/need overrides, not profit", cite="Exod 20:8-10 (kept)"),

    # ── genuinely HARD cases: even the hybrid mis-fires (honest ceiling) ──────
    "RichYoungRuler": dict(facts={"relievesNeed", "ownCostly"}, verdict="allowed",
                           ratio="sell all and give — a counsel of perfection, not a strict duty "
                                 "for all (hybrid over-obligates)", cite="Mark 10:17-22"),
    "OxInPit": dict(facts={"breaksSabbath", "minorNeed"}, verdict="allowed",
                    ratio="pull the ox from the pit on the sabbath — a minor-need exception "
                          "the formal theory lacks (hybrid over-forbids)", cite="Luke 14:5"),
}

FACT_ATOMS = sorted({f for e in EPISODES.values() for f in e["facts"]})


def sanity_unique():
    """No two episodes share an identical fact vector with different verdicts."""
    seen = {}
    for name, e in EPISODES.items():
        key = frozenset(e["facts"])
        if key in seen and seen[key][1] != e["verdict"]:
            raise AssertionError(f"contradiction: {name} vs {seen[key][0]} on {set(key)}")
        seen[key] = (name, e["verdict"])
    return True


if __name__ == "__main__":
    sanity_unique()
    from collections import Counter
    print(f"{len(EPISODES)} episodes, {len(FACT_ATOMS)} fact atoms")
    print("verdicts:", dict(Counter(e["verdict"] for e in EPISODES.values())))
    print("fact atoms:", FACT_ATOMS)
