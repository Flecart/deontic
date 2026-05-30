"""Phase B — evolved case law with a REAL (fallible) LLM judge.

For each selected theory: (1) measure the LLM judge's own verdict accuracy vs the
latent law over all cases; (2) feed its rulings to the case-law institution and
measure held-out generalization; (3) compare to the oracle-judge result. This
shows how judge fallibility propagates into evolved law.
"""
from __future__ import annotations

import itertools
import json
import os
import random
import statistics

from . import theories
from .experiment import all_cases, atom_decls, split, _acc, run_arm
from .institutions import CaseLawInstitution
from .llm_judge import LLMJudge

THEORIES_B = ["T02_exception", "T03_nested", "T05_duty", "T08_license", "T09_externality"]
MODEL = os.environ.get("CASELAW_JUDGE_MODEL", "openai/gpt-4o-mini")


def run_theory(tname, seed=0, repeats=3):
    T = theories.THEORIES[tname]
    facts, tgt, ddl = T["facts"], T["target"], T["ddl"]
    cases = all_cases(facts)
    judge = LLMJudge(tname, ddl, tgt, facts, model=MODEL)
    # 1) judge's own accuracy over all cases
    judge_acc = sum(judge.rule(c) == judge.truth(c) for c in cases) / len(cases)
    # 2) evolved case law from the LLM's rulings
    inst = CaseLawInstitution(atom_decls(ddl), tgt, facts)
    train, test = split(cases, seed)
    stream = train * repeats
    random.Random(seed).shuffle(stream)
    for c in stream:
        v = judge.rule(c)
        if v.startswith("__ERR__"):
            continue
        inst.learn(c, v)
    law_test = _acc(inst, test, judge)
    law_full = _acc(inst, cases, judge)
    # 3) oracle baseline
    orc = run_arm("caselaw", T, 0.0, seed)
    return {"judge_acc": round(judge_acc, 3), "law_test_acc": round(law_test, 3),
            "law_full_acc": round(law_full, 3), "oracle_test_acc": round(orc["test_acc"], 3),
            "rule_count": inst.size(), "api_calls": judge.calls}


def main():
    out = {}
    for t in THEORIES_B:
        try:
            out[t] = run_theory(t)
        except Exception as exc:  # noqa
            out[t] = {"error": f"{type(exc).__name__}: {exc}"}
        print(t, out[t], flush=True)
    path = os.path.join(os.path.dirname(__file__), "runs", "phaseB.json")
    json.dump({"model": MODEL, "results": out}, open(path, "w"), indent=2)
    print("wrote", path)


if __name__ == "__main__":
    main()
