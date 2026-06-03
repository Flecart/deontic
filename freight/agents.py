"""Agents: the settlement / filing strategy layer.

The game-theoretic primitive (Priest-Rubin): each party holds a *prior* over how
J would rule, and litigates only when those priors diverge enough to destroy the
settlement surplus. We ground both priors in the SAME object J consults -- the
breach rate among the precedents retrieved for this case -- then add each party's
self-serving optimism and a sliver of private information (the seller knows its
cost shock theta, the buyer its valuation noise eta). Convergent, consistent
precedent => convergent priors => settlement; thin or contradictory precedent on
a borderline case => divergent priors => a filed case.

  Settlement zone exists  iff  (p_B - p_S) * d_hat * price <= c_f
  Buyer files (no zone)    iff  p_B * d_hat * price - c_f > 0   (case not hopeless)

So filings select for high prior-divergence -- the ambiguity frontier. As C
matures the divergence shrinks and filing decays. Stub agents short-circuit all
of this and file every transaction, to exercise the corpus machinery alone.
"""
from __future__ import annotations

import random

from . import env


def _precedent_prior(corpus, txn, k=5) -> tuple[float, float, int, float]:
    """Similarity-weighted breach rate `base`, mean breach-damage `d_hat`, count,
    and an *unsettledness* `u` in [0,1]: how unpredictable J's ruling is on these
    facts given the precedent. u is high when precedent is sparse or a coin-flip
    (the ambiguity frontier) and ~0 when precedent agrees -- this is what makes
    priors converge, and litigation decay, as the corpus matures."""
    prec = [c for c in corpus.retrieve(txn["facts"], k=k)
            if c.get("ruling") in ("compliant", "breach")]
    if len(prec) < 2:
        # thin precedent: maximally unsettled, anchored on structural ambiguity.
        base = 0.5 if txn["ambiguity"] > 0.5 else (0.8 if txn["severity"] > 0.5 else 0.2)
        return base, 0.4, len(prec), 1.0
    w = [max(0.0, c.get("_sim", 0.0)) + 1e-3 for c in prec]
    wsum = sum(w)
    base = sum(wi for wi, c in zip(w, prec) if c["ruling"] == "breach") / wsum
    dmgs = [c.get("damage", 0.4) for c in prec if c["ruling"] == "breach"]
    d_hat = sum(dmgs) / len(dmgs) if dmgs else 0.4
    # coin-flip-ness (peaks at base=0.5), damped when precedent is plentiful.
    u = 4.0 * base * (1.0 - base)
    u = max(u, 1.0 / (1.0 + len(prec)))      # residual uncertainty from sparsity
    return base, d_hat, len(prec), min(1.0, u)


class StubAgents:
    """Both parties file on every transaction (de-risking harness)."""
    strategic = False

    def interact(self, corpus, txn, c_f, rng) -> dict:
        return {"filed": True, "settled": False, "r": 0.0,
                "p_B": None, "p_S": None, "d_hat": None, "n_prec": len(corpus),
                "reason": "stub: always file"}


class StrategicAgents:
    def __init__(self, optimism=0.12, info_noise=0.06):
        self.optimism = optimism      # self-serving bias on the prior
        self.info_noise = info_noise  # private-information jitter
        self.strategic = True

    def interact(self, corpus, txn, c_f, rng: random.Random) -> dict:
        base, d_hat, n_prec, u = _precedent_prior(corpus, txn)
        # Self-serving optimism and private information bite only to the extent
        # the law is unsettled (u): on a predictable case both sides agree on
        # base, the surplus survives, and they settle.
        s_info = -0.05 * (txn["theta"] - 1.0)            # seller's force-majeure story
        b_info = 0.05 * max(0.0, -txn["eta"])            # buyer's disappointment
        spread = self.optimism * u
        p_B = _clip(base + spread + u * (b_info + rng.gauss(0, self.info_noise)))
        p_S = _clip(base - spread + u * (s_info + rng.gauss(0, self.info_noise)))
        price = txn["price"]
        # bargaining endpoints
        buyer_floor = p_B * d_hat * price - c_f       # min settlement buyer accepts
        seller_ceiling = p_S * d_hat * price          # max settlement seller pays
        zone = seller_ceiling - buyer_floor           # >=0 => settlement possible
        if zone >= 0:
            r = _clip(0.5 * (buyer_floor + seller_ceiling), 0.0, price)
            return {"filed": False, "settled": True, "r": round(r, 2),
                    "p_B": round(p_B, 3), "p_S": round(p_S, 3),
                    "d_hat": round(d_hat, 3), "n_prec": n_prec,
                    "reason": "settled"}
        # no zone: litigate iff the buyer's case is not hopeless.
        if buyer_floor > 0:
            return {"filed": True, "settled": False, "r": 0.0,
                    "p_B": round(p_B, 3), "p_S": round(p_S, 3),
                    "d_hat": round(d_hat, 3), "n_prec": n_prec,
                    "reason": "diverged priors -> file"}
        return {"filed": False, "settled": True, "r": 0.0,
                "p_B": round(p_B, 3), "p_S": round(p_S, 3),
                "d_hat": round(d_hat, 3), "n_prec": n_prec,
                "reason": "buyer walks (hopeless)"}


def seller_deviation(theta: float, liability_aversion: float, rng: random.Random) -> float:
    """How far S is willing to deviate, given its cost shock and an aversion to
    expected liability. High theta tempts deviation; aversion pulls it back."""
    appetite = (theta - 1.0) * 0.9 + rng.uniform(-0.1, 0.1)
    return max(0.0, min(1.0, appetite - liability_aversion * 0.3))


def _clip(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))
