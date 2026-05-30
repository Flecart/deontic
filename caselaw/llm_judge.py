"""Phase B — a real LLM judge.

The LLM is given a short natural-language statement of a theory's law and asked
to rule on each case (forbidden / obligatory / allowed / dilemma). Its (fallible)
rulings feed the SAME case-law institution as Phase A, so we measure: how good is
evolved case law when the judge is a real model interpreting an NL statute, and
how does its accuracy compare to the oracle judge?

Keys: OPENAI_API_KEY / OPENROUTER_API_KEY in the environment.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache

# Natural-language statutes (what a judge is told the law is). The judge never
# sees the formal latent theory — it must apply these in prose.
NL_STATUTE = {
    "T01_absolute": "Performing the action is always forbidden, with no exceptions.",
    "T02_exception": "Performing the action is forbidden, UNLESS there is a genuine emergency, in which case it is allowed.",
    "T03_nested": "The action is forbidden. A genuine emergency makes it allowed — but if the actor was reckless, it is forbidden again even in an emergency.",
    "T04_competing": "The action is forbidden by default. A standing entitlement makes it allowed. But if the action concretely harms others, it is forbidden regardless of entitlement.",
    "T05_duty": "If a hazard requiring report is present, performing the action (reporting) is OBLIGATORY. Otherwise it is merely allowed.",
    "T06_compensation": "(Target: remediate.) If the actor performed the act, remediating the harm is OBLIGATORY; otherwise remediation is merely allowed.",
    "T07_repeat": "(Target: restrain.) If the actor has a prior offense on record, additionally restraining is OBLIGATORY; otherwise it is merely allowed.",
    "T08_license": "The action is forbidden UNLESS the actor both holds a valid licence AND gave the required prior notice; only then is it allowed.",
    "T09_externality": "The action is allowed by default. It becomes forbidden only when the shared resource is stressed — unless the affected parties consented, which makes it allowed again.",
    "T10_dilemma": "If ground A applies, the action is obligatory. If ground B applies, it is forbidden. If both apply at once, it is a genuine dilemma with no resolution.",
}

_SYS = ("You are a judge applying a fixed statute to a concrete case. Read the "
        "statute and the facts, then output STRICT JSON: "
        '{"verdict": one of "forbidden"|"obligatory"|"allowed"|"dilemma"}. '
        "Decide only from the statute; ignore facts the statute does not mention.")


def _client_for(model):
    from openai import OpenAI
    if model.startswith("openai/"):
        return OpenAI(api_key=os.environ["OPENAI_API_KEY"]), model.split("/", 1)[1]
    return (OpenAI(api_key=os.environ["OPENROUTER_API_KEY"],
                   base_url="https://openrouter.ai/api/v1"), model)


class LLMJudge:
    def __init__(self, theory_name, latent_ddl, target, fact_atoms, model="openai/gpt-4o-mini"):
        from . import engine
        self.tname, self.latent, self.target = theory_name, latent_ddl, target
        self.fact_atoms, self.model = list(fact_atoms), model
        self._engine = engine
        self._client, self._mid = _client_for(model)
        self.calls = 0

    def truth(self, case):  # ground truth = the latent law
        return self._engine.verdict(self.latent, case, self.target)

    @lru_cache(maxsize=4096)
    def _ask(self, case_key):
        present = [f for f in self.fact_atoms if f in case_key]
        absent = [f for f in self.fact_atoms if f not in case_key]
        user = (f"STATUTE: {NL_STATUTE[self.tname]}\n\n"
                f"FACTS PRESENT: {', '.join(present) or '(none)'}\n"
                f"FACTS ABSENT: {', '.join(absent) or '(none)'}\n\n"
                "Output the JSON verdict now.")
        try:
            kw = {"model": self._mid,
                  "messages": [{"role": "system", "content": _SYS},
                               {"role": "user", "content": user}]}
            if not self._mid.startswith(("o", "gpt-5")):
                kw["temperature"] = 0.0
            r = self._client.chat.completions.create(**kw)
            self.calls += 1
            txt = r.choices[0].message.content or ""
            for v in ("forbidden", "obligatory", "allowed", "dilemma"):
                if f'"{v}"' in txt or f": {v}" in txt.lower():
                    return v
            return "allowed"
        except Exception as exc:  # noqa
            return f"__ERR__{type(exc).__name__}"

    def rule(self, case):
        return self._ask(frozenset(case))
