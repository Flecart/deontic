"""Natural-language rendering of theories and conclusions (the audit
round-trip). Lets a human or an LLM verify *"did I formalise this faithfully?"*
and read verdicts back in plain English.
"""

from __future__ import annotations

from .proof import Conclusion
from .syntax import BodyElem, Literal, ModalLiteral, Rule, Theory, is_bottom

_OP_PHRASE = {
    "O": "it is obligatory that {}",
    "P": "it is permitted that {}",
    "Pw": "it is weakly permitted that {}",
    "Ps": "it is strongly permitted that {}",
}


def phrase_literal(l: Literal) -> str:
    if is_bottom(l):
        return "a non-compensable violation"
    return f"not {l.atom}" if l.negated else l.atom


def phrase_elem(b: BodyElem) -> str:
    if isinstance(b, ModalLiteral):
        inner = phrase_literal(b.lit)
        if b.op == "O" and b.lit.negated:
            base = f"{b.lit.atom} is forbidden"
        else:
            base = _OP_PHRASE[b.op].format(inner)
        return f"it is not the case that {base}" if b.negated else base
    return phrase_literal(b)


def describe_rule(r: Rule) -> str:
    kind = "defeater" if r.is_defeater else "rule"
    family = "constitutive" if r.mode == "C" else "prescriptive"
    if r.body:
        cond = " and ".join(phrase_elem(b) for b in r.body)
        cond = f"if {cond}, then "
    else:
        cond = ""
    if r.mode == "O":
        chain = r.head
        primary = chain[0]
        head = (
            f"{primary.atom} is forbidden"
            if primary.negated
            else f"it is obligatory that {primary.atom}"
        )
        if len(chain) > 1:
            comps = ", failing which ".join(phrase_literal(c) for c in chain[1:])
            head += f" (compensated, in order, by: {comps})"
    else:
        head = f"it counts as {phrase_literal(r.head[0])}"
    return f"{r.label} [{family} {kind}]: {cond}{head}"


def describe_conclusion(c: Conclusion) -> str:
    if c.modality == "⊥":
        if c.positive:
            return "the situation is NON-COMPLIANT (a non-compensable violation occurred)"
        return "the situation is compliant (no non-compensable violation)"
    l = c.literal
    if c.modality == "C":
        body = phrase_literal(l)
        return f"{body} holds" if c.positive else f"{body} is not provable"
    if c.modality == "O":
        if l.negated:
            base = f"{l.atom} is forbidden (F {l.atom})"
        else:
            base = f"{l.atom} is obligatory (O {l.atom})"
    else:
        label = {"P": "permitted", "Pw": "weakly permitted", "Ps": "strongly permitted"}[
            c.modality
        ]
        base = f"{phrase_literal(l)} is {label} ({c.modality} {l})"
    return base if c.positive else f"it is NOT the case that {base}"


def describe_theory(theory: Theory) -> str:
    lines: list[str] = []
    if theory.facts:
        facts = ", ".join(sorted(phrase_literal(f) for f in theory.facts))
        lines.append(f"Facts: {facts}.")
    if theory.rules:
        lines.append("Norms:")
        for r in theory.rules:
            lines.append(f"  - {describe_rule(r)}")
    if theory.superiority:
        lines.append("Priorities:")
        for weaker, stronger in sorted(theory.superiority):
            lines.append(f"  - {stronger} overrides {weaker}")
    return "\n".join(lines)
