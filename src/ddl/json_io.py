"""Structured-JSON theory interface -- the LLM-facing front end.

Self-documenting field names instead of the terse DSL operators, so a model can
emit a theory by tool call and get targeted validation errors. The JSON and the
``.ddl`` DSL compile to the same AST.

Theory shape::

    {
      "facts": ["license", "publish"],
      "rules": [
        {"id": "r2", "kind": "prescriptive", "strength": "defeasible",
         "if": [], "then": {"obligation": ["-publish", "remove"]},
         "gloss": "Publishing is forbidden; removing compensates."},
        {"id": "c31", "kind": "constitutive",
         "if": ["highSpend"], "then": {"counts_as": "premiumCustomer"}}
      ],
      "superiority": [["r0", "r1"]]      // r0 < r1: r1 overrides r0
    }

* ``if`` entries are literals/modal literals in DSL token form: ``"highSpend"``,
  ``"-surcharge"``, ``"P publish"``, ``"O remove"``, ``"F publish"``.
* ``then`` is one of: ``{"obligation": [...]}`` (an otimes chain),
  ``{"forbidden": "x"}`` (= obligation of ~x), ``{"counts_as": "x"}``
  (constitutive), or a bare string (constitutive unless ``kind`` says otherwise).
* ``kind`` defaults to constitutive for ``counts_as``/bare strings and
  prescriptive for ``obligation``/``forbidden``. ``strength`` defaults to
  ``defeasible`` (use ``defeater`` for a blocking-only rule).
"""

from __future__ import annotations

import json

from .parser import ParseError, _parse_body_elem, _parse_literal
from .syntax import Literal, ModalLiteral, Rule, Theory, normalize_chain


def theory_from_json(data: dict | str) -> Theory:
    if isinstance(data, str):
        data = json.loads(data)
    if not isinstance(data, dict):
        raise ParseError("theory JSON must be an object")
    theory = Theory()
    for f in data.get("facts", []):
        theory.facts.add(_parse_literal(f))
    labels: set[str] = set()
    for i, rd in enumerate(data.get("rules", [])):
        rule = _rule_from_json(rd, i)
        if rule.label in labels:
            raise ParseError(f"duplicate rule id {rule.label!r}")
        labels.add(rule.label)
        theory.rules.append(rule)
    for pair in data.get("superiority", []):
        if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
            raise ParseError(f"superiority entry must be a pair, got {pair!r}")
        weaker, stronger = pair
        for ref in (weaker, stronger):
            if ref not in labels:
                raise ParseError(f"superiority {pair} references unknown rule {ref!r}")
        theory.superiority.add((weaker, stronger))
    return theory


def _rule_from_json(rd: dict, i: int) -> Rule:
    if not isinstance(rd, dict):
        raise ParseError(f"rule #{i + 1} must be an object, got {rd!r}")
    label = rd.get("id") or f"r{i + 1}"
    strength = rd.get("strength", "defeasible")
    if strength not in ("defeasible", "defeater"):
        raise ParseError(f"rule {label!r}: strength must be defeasible|defeater")
    try:
        body = tuple(_parse_body_elem(b) for b in rd.get("if", []))
    except ParseError as e:
        raise ParseError(f"rule {label!r}: {e}") from e
    if "then" not in rd:
        raise ParseError(f"rule {label!r}: missing 'then'")
    mode, head = _head_from_json(rd["then"], rd.get("kind"), label)
    return Rule(label, mode, strength, body, head, gloss=rd.get("gloss", ""))


def _head_from_json(then, kind, label: str) -> tuple[str, tuple[Literal, ...]]:
    if isinstance(then, str):
        mode = "O" if kind == "prescriptive" else "C"
        return mode, (_parse_literal(then),)
    if isinstance(then, dict):
        if "obligation" in then:
            chain = then["obligation"]
            if isinstance(chain, str):
                chain = [chain]
            return "O", normalize_chain(tuple(_parse_literal(x) for x in chain))
        if "forbidden" in then:
            return "O", (_parse_literal(then["forbidden"]).complement,)
        if "counts_as" in then:
            return "C", (_parse_literal(then["counts_as"]),)
    raise ParseError(
        f"rule {label!r}: 'then' must be a string or have one of "
        f"'obligation'/'forbidden'/'counts_as', got {then!r}"
    )


# ---------------------------------------------------------------- serialisation
def _elem_to_token(b) -> str:
    if isinstance(b, ModalLiteral):
        prefix = "-" if b.negated else ""
        return f"{prefix}{b.op} {b.lit}"
    return str(b)


def rule_to_json(r: Rule) -> dict:
    out: dict = {"id": r.label, "strength": r.strength}
    out["if"] = [_elem_to_token(b) for b in r.body]
    if r.mode == "C":
        out["kind"] = "constitutive"
        out["then"] = {"counts_as": str(r.head[0])}
    else:
        out["kind"] = "prescriptive"
        out["then"] = {"obligation": [str(h) for h in r.head]}
    if r.gloss:
        out["gloss"] = r.gloss
    return out


def theory_to_json(theory: Theory) -> dict:
    return {
        "facts": sorted(str(f) for f in theory.facts),
        "rules": [rule_to_json(r) for r in theory.rules],
        "superiority": [list(p) for p in sorted(theory.superiority)],
    }
