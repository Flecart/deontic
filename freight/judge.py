"""J -- the LLM-as-judge with retrieval over the corpus C.

J reads the thin seed law Omega_0, retrieves the top-k most similar prior cases
from C by embedding similarity on the facts field, and renders a judgment:
ruling in {compliant, breach} and a damage fraction in [0,1] of the price.

It is deliberately *grounded in precedent*: when C is empty it falls back on
Omega_0 alone; as C matures it is pulled toward the holdings it retrieves. That
feedback is the whole point -- the law J applies is the law prior J's made.
"""
from __future__ import annotations

import json
import os
import re

from . import corpus as corpus_mod

OMEGA0_TEXT = "\n".join(f"- {p}" for p in corpus_mod.OMEGA0)

_SYS = (
    "You are J, the judge in a freight/sales dispute under a UCC-Article-2-style "
    "regime for an agent society. You decide whether the seller's delivery is a "
    "lawful performance (compliant) or a breach, and if a breach, the damages owed "
    "as a fraction of the contract price.\n\n"
    "Apply, in order: (1) the retrieved precedents -- follow them where the facts "
    "are alike (stare decisis); (2) the seed law; (3) commercial reasonableness. "
    "Decide only from the facts given.\n\n"
    "Output STRICT JSON and nothing else: "
    '{"ruling": "compliant"|"breach", "damage": <0..1>, "rationale": "<one sentence>"}'
)


class Judge:
    def __init__(self, corpus, model="gpt-4o-mini", k=5):
        self.corpus = corpus
        self.model = model
        self.k = k
        self.calls = 0
        from openai import OpenAI
        self._cli = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def _prompt(self, facts: str) -> list[dict]:
        prec = self.corpus.retrieve(facts, k=self.k)
        if prec:
            block = "\n\n".join(
                f"[precedent {i+1}, sim={c.get('_sim', 0):.2f}] {c['facts']}\n"
                f"   -> RULING: {c['ruling']}"
                + (f", damage {c.get('damage', 0):.0%} of price" if c['ruling'] == 'breach' else "")
                + (f". {c.get('rationale','')}" if c.get('rationale') else "")
                for i, c in enumerate(prec))
        else:
            block = "(no precedents yet -- decide on the seed law alone)"
        user = (f"SEED LAW (Omega_0):\n{OMEGA0_TEXT}\n\n"
                f"RETRIEVED PRECEDENTS:\n{block}\n\n"
                f"CASE BEFORE YOU:\n{facts}\n\nOutput the JSON ruling now.")
        return [{"role": "system", "content": _SYS}, {"role": "user", "content": user}]

    def _ask(self, facts: str, temperature: float) -> dict:
        kw = dict(model=self.model, messages=self._prompt(facts))
        if not self.model.startswith(("o", "gpt-5")):
            kw["temperature"] = temperature
        try:
            r = self._cli.chat.completions.create(**kw)
            self.calls += 1
            return _parse(r.choices[0].message.content or "")
        except Exception as exc:  # noqa
            return {"ruling": "compliant", "damage": 0.0,
                    "rationale": f"__ERR__{type(exc).__name__}"}

    def rule(self, txn: dict) -> dict:
        """Render a judgment on a transaction. Returns the ruling dict, scaled to
        an absolute damage amount in `damage_abs`."""
        out = self._ask(txn["facts"], temperature=0.0)
        out["damage"] = float(max(0.0, min(1.0, out.get("damage", 0.0))))
        if out["ruling"] != "breach":
            out["damage"] = 0.0
        out["damage_abs"] = round(out["damage"] * txn["price"], 2)
        return out

    def self_consistency(self, txn: dict, n: int = 3) -> float:
        """Predictability metric: resample the ruling at temperature and report
        the modal-agreement fraction (1.0 = perfectly self-consistent)."""
        votes = [self._ask(txn["facts"], temperature=0.8)["ruling"] for _ in range(n)]
        votes = [v for v in votes if not str(v).startswith("__ERR__")]
        if not votes:
            return float("nan")
        top = max(set(votes), key=votes.count)
        return votes.count(top) / len(votes)


def _parse(txt: str) -> dict:
    m = re.search(r"\{.*\}", txt, re.S)
    if m:
        try:
            d = json.loads(m.group(0))
            r = "breach" if str(d.get("ruling", "")).lower().startswith("breach") else "compliant"
            return {"ruling": r, "damage": float(d.get("damage", 0.0) or 0.0),
                    "rationale": str(d.get("rationale", ""))[:200]}
        except Exception:  # noqa
            pass
    low = txt.lower()
    return {"ruling": "breach" if "breach" in low else "compliant",
            "damage": 0.3 if "breach" in low else 0.0, "rationale": txt[:120]}
