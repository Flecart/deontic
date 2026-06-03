"""The one-shot freight/sales game world.

A buyer B and seller S contract over a structured spec `x` with crisp fields
(quantity, deadline, price) and fuzzy fields (quality, packaging, substitution
clause, force-majeure clause). After contracting, S draws a private cost shock
theta and chooses a delivery `x'` that may deviate on the fuzzy dimensions; B
draws private valuation noise eta and realises value v(x', eta).

This module owns ONLY the physical world: how contracts and deliveries are
sampled, what they cost, what they are worth, and a UCC-grounded *oracle* ruling
used to score held-out accuracy. The settlement/filing strategy lives in
`agents.py`; the (fallible) LLM ruling lives in `judge.py`.

The design lens (see CLAUDE.md): this is norms for an LLM agent society, not real
legal practice. We own the vocabulary, so the fuzzy clauses are drawn from a small
shared template bank rather than free text.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, asdict

# --- the spec space ---------------------------------------------------------
# 7 good classes x {standard, premium} x 3 windows x 3 packaging x 4 substitution
# x 4 force-majeure ~= 2k discrete shells, plus continuous quantity/price.

GOODS = ["grain", "steel_coil", "lumber", "textile", "polymer_resin",
         "citrus", "microcontrollers"]
TIERS = ["standard", "premium"]
WINDOWS = [7, 14, 30]                 # promised delivery window, days
PACKAGING = ["bulk", "palletized", "retail_ready"]

# Substitution clauses, ordered by how much deviation they tolerate (0..1 = the
# clause's *permissiveness*). A permissive clause forgives more deviation.
SUBSTITUTION = {
    "strict_identity":   0.05,   # "exact goods as specified; no substitutes"
    "like_kind":         0.35,   # "substitutes of like kind and quality allowed"
    "commercially_reas": 0.65,   # UCC 2-306-style commercial reasonableness
    "seller_option":     0.90,   # "seller may substitute at its discretion"
}
# Force-majeure clauses, by how much they excuse a cost shock (0..1).
FORCE_MAJEURE = {
    "none":              0.00,
    "acts_of_god":       0.30,   # narrow: natural events only
    "impracticability":  0.60,   # UCC 2-615 commercial impracticability
    "broad_hardship":    0.85,   # any material hardship excuses performance
}

# The deviation dimensions a seller can move on, and their per-unit "severity".
DEV_DIMS = ["quality", "packaging", "lateness", "shortfall", "substitute"]


@dataclass(frozen=True)
class Contract:
    good: str
    tier: str
    window: int          # promised days
    packaging: str
    substitution: str    # key into SUBSTITUTION
    force_majeure: str   # key into FORCE_MAJEURE
    quantity: int
    price: float         # total contract price p

    @property
    def permissiveness(self) -> float:
        return SUBSTITUTION[self.substitution]


@dataclass(frozen=True)
class Delivery:
    """What S actually shipped, as deviations from the contract (each in [0,1],
    0 = perfect tender on that dimension)."""
    quality_drop: float     # downgrade premium->standard etc.
    packaging_change: float
    lateness: float         # fraction of window overrun
    shortfall: float        # fraction of quantity missing
    substitute: float       # how unlike the contracted good

    def severity(self) -> float:
        # weighted aggregate deviation; substitution/quality weigh most.
        w = {"quality_drop": 1.0, "packaging_change": 0.4, "lateness": 0.7,
             "shortfall": 0.9, "substitute": 1.0}
        s = (w["quality_drop"] * self.quality_drop
             + w["packaging_change"] * self.packaging_change
             + w["lateness"] * self.lateness
             + w["shortfall"] * self.shortfall
             + w["substitute"] * self.substitute)
        return s / sum(w.values())


def sample_contract(rng: random.Random) -> Contract:
    qty = rng.choice([100, 250, 500, 1000, 2000])
    unit = round(rng.uniform(2.0, 50.0), 2)
    return Contract(
        good=rng.choice(GOODS),
        tier=rng.choice(TIERS),
        window=rng.choice(WINDOWS),
        packaging=rng.choice(PACKAGING),
        substitution=rng.choice(list(SUBSTITUTION)),
        force_majeure=rng.choice(list(FORCE_MAJEURE)),
        quantity=qty,
        price=round(qty * unit, 2),
    )


def cost_shock(rng: random.Random) -> float:
    """theta ~ F: a multiplicative cost shock, lognormal-ish, mean ~1, fat upper
    tail (occasional supply crunches that tempt deviation)."""
    return float(min(3.0, max(0.4, rng.lognormvariate(0.0, 0.45))))


def choose_delivery(c: Contract, theta: float, rng: random.Random,
                    deviate: float | None = None) -> Delivery:
    """S's physical choice. `deviate` in [0,1] is the strategic appetite for
    deviation (set by the agent layer); when None we draw it from theta so that
    high cost shocks push toward deviating. Deviation is concentrated on the
    dimensions the contract's clauses most tolerate."""
    if deviate is None:
        deviate = max(0.0, min(1.0, (theta - 1.0) * 0.8 + rng.uniform(-0.1, 0.1)))
    # The seller deviates more where it is cheaper to (permissive substitution)
    # and where force majeure offers cover.
    cover = 0.5 * c.permissiveness + 0.5 * FORCE_MAJEURE[c.force_majeure]
    scale = deviate * (0.5 + 0.5 * cover)

    def d(bias):
        return round(max(0.0, min(1.0, scale * bias * rng.uniform(0.6, 1.4))), 3)

    return Delivery(
        quality_drop=d(1.0 if c.tier == "premium" else 0.5),
        packaging_change=d(0.6),
        lateness=d(0.8 if theta > 1.2 else 0.3),
        shortfall=d(0.5),
        substitute=d(1.0 if c.permissiveness > 0.3 else 0.3),
    )


def cost(c: Contract, d: Delivery, theta: float) -> float:
    """S's realised cost. Baseline is a fraction of price; the cost shock raises
    it; deviating (cutting corners) lowers it. This is why S is tempted."""
    base = 0.7 * c.price
    saved = d.severity() * 0.35 * c.price          # corner-cutting savings
    return round(theta * base - saved, 2)


def value(c: Contract, d: Delivery, eta: float) -> float:
    """B's realised value. Perfect tender is worth a markup over price; deviation
    destroys value; eta is private taste noise."""
    base = 1.25 * c.price
    lost = d.severity() * 0.6 * c.price
    return round(base - lost + eta * 0.1 * c.price, 2)


def valuation_noise(rng: random.Random) -> float:
    return round(rng.gauss(0.0, 1.0), 3)


# --- ambiguity & oracle -----------------------------------------------------

def ambiguity(c: Contract, d: Delivery) -> float:
    """How borderline is this (x, x') pair, in [0,1]?

    A ruling is *clear* when the deviation is plainly inside what the clauses
    permit (compliant) or plainly outside (breach). It is *ambiguous* when the
    deviation severity sits right at the margin the clause language tolerates.
    We model the clause as licensing severity up to `permissiveness`; ambiguity
    peaks where severity ~= that threshold. Force majeure widens the grey zone
    (it gives the seller a second, contestable excuse)."""
    threshold = 0.15 + 0.7 * c.permissiveness
    margin = abs(d.severity() - threshold)
    # triangular peak at the threshold, widened by force-majeure cover.
    width = 0.18 + 0.25 * FORCE_MAJEURE[c.force_majeure]
    return round(max(0.0, 1.0 - margin / width), 3)


def oracle_ruling(c: Contract, d: Delivery) -> tuple[str, float]:
    """A UCC-grounded 'correct' ruling, used only to score held-out accuracy on
    the labelled subset. Not visible to agents or the LLM judge.

    Simplified doctrine:
      * Perfect tender baseline (UCC 2-601): material deviation is breach...
      * ...unless licensed by the substitution clause's commercial-reasonableness
        allowance (2-306 / 2-314) up to its permissiveness threshold, or excused
        by force majeure (2-615 impracticability) scaled by the cost shock.
    Damage d is expectation-style: the value the deviation destroyed, capped at p.
    """
    sev = d.severity()
    licensed = 0.15 + 0.7 * c.permissiveness
    excused = FORCE_MAJEURE[c.force_majeure] * 0.25
    if sev <= licensed + excused:
        return "compliant", 0.0
    over = sev - (licensed + excused)
    dmg = round(min(1.0, 0.6 * over + 0.3) * c.price, 2)
    return "breach", dmg


# --- text rendering (the 'facts' field used for retrieval) ------------------

def facts_text(c: Contract, d: Delivery) -> str:
    """A compact natural-language statement of the facts. This is what J reads,
    what gets embedded for retrieval, and what defines the ambiguity axis."""
    def lvl(x):
        return "none" if x < 0.05 else "minor" if x < 0.25 else \
               "moderate" if x < 0.55 else "major"
    return (
        f"Contract: {c.quantity} units of {c.tier} {c.good}, "
        f"${c.price:.0f}, delivery within {c.window} days, {c.packaging} packaging. "
        f"Substitution clause: {c.substitution.replace('_', ' ')}. "
        f"Force-majeure clause: {c.force_majeure.replace('_', ' ')}.\n"
        f"Delivery deviations -- quality downgrade: {lvl(d.quality_drop)}; "
        f"packaging change: {lvl(d.packaging_change)}; "
        f"lateness: {lvl(d.lateness)}; "
        f"quantity shortfall: {lvl(d.shortfall)}; "
        f"good substituted: {lvl(d.substitute)}."
    )


def assemble(c: Contract, d: Delivery, theta: float, eta: float) -> dict:
    """Build a transaction record from an explicit contract + delivery (used by
    the held-out welfare eval, where the seller optimises its deviation rather
    than drawing it). Mirrors `transaction` but takes the physical choice as given."""
    v = value(c, d, eta)
    cst = cost(c, d, theta)
    return {
        "contract": asdict(c), "delivery": asdict(d),
        "theta": round(theta, 3), "eta": eta,
        "value": v, "cost": cst, "price": c.price,
        "severity": round(d.severity(), 3),
        "ambiguity": ambiguity(c, d),
        "permissiveness": c.permissiveness,
        "fm": FORCE_MAJEURE[c.force_majeure],
        "facts": facts_text(c, d),
        "oracle": dict(zip(("ruling", "damage"), oracle_ruling(c, d))),
        "_c": c, "_d": d,
    }


def transaction(rng: random.Random, deviate: float | None = None) -> dict:
    """Draw a full transaction: contract, shock, delivery, value. Returns a plain
    dict (JSONL-friendly) plus the live dataclasses under '_c'/'_d'."""
    c = sample_contract(rng)
    theta = cost_shock(rng)
    d = choose_delivery(c, theta, rng, deviate=deviate)
    eta = valuation_noise(rng)
    v = value(c, d, eta)
    cst = cost(c, d, theta)
    return {
        "contract": asdict(c), "delivery": asdict(d),
        "theta": round(theta, 3), "eta": eta,
        "value": v, "cost": cst, "price": c.price,
        "severity": round(d.severity(), 3),
        "ambiguity": ambiguity(c, d),
        "permissiveness": c.permissiveness,
        "fm": FORCE_MAJEURE[c.force_majeure],
        "facts": facts_text(c, d),
        "oracle": dict(zip(("ruling", "damage"), oracle_ruling(c, d))),
        "_c": c, "_d": d,
    }
