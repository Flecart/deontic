"""High-level library facade: load a theory, ask a tagged-literal query, get a
verdict with a natural-language proof trace.

This is the entry point intended for embedding (CLI, LLM tool layer). The LLM
formalises norms (via JSON or DSL), the engine reasons deterministically, and
the verdict + trace are handed back for the LLM to verbalise.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .engine import Extension, extension
from .json_io import theory_from_json
from .parser import _parse_literal, parse
from .proof import Conclusion
from .render import describe_conclusion, describe_theory
from .syntax import BOTTOM, BodyElem, Literal, ModalLiteral, Theory, is_bottom

_TAG_RE = re.compile(r"^([+-])?d(C|O|Ps|Pw|P)\s+(.+)$")
_FRIENDLY_RE = re.compile(r"^(O|F|Pw|Ps|P)\s+(.+)$")
_BOTTOM_POS = {"+d_bottom", "+dbottom", "+d⊥", "bottom", "noncompliant", "non-compliant"}
_BOTTOM_NEG = {"-d_bottom", "-dbottom", "-d⊥", "compliant"}
_VACUOUS_POS = {"C": False, "O": False, "Pw": True, "Ps": False, "P": True}


def parse_query(text: str) -> Conclusion:
    """Parse a query into a target Conclusion. Accepts the tag form
    (``+dO remove``, ``-dC publish``), the friendly form (``O remove``,
    ``F publish``, ``P use``), ``bottom``/``compliant``, or a bare literal
    (``publish`` == ``+dC publish``)."""
    t = text.strip()
    low = t.lower()
    if low in _BOTTOM_POS:
        return Conclusion("+", "⊥", BOTTOM)
    if low in _BOTTOM_NEG:
        return Conclusion("-", "⊥", BOTTOM)
    m = _TAG_RE.match(t)
    if m:
        return Conclusion(m.group(1) or "+", m.group(2), _parse_literal(m.group(3)))
    m = _FRIENDLY_RE.match(t)
    if m:
        op, rest = m.group(1), _parse_literal(m.group(2))
        if op == "F":
            return Conclusion("+", "O", rest.complement)
        return Conclusion("+", "O" if op == "O" else op, rest)
    return Conclusion("+", "C", _parse_literal(t))


@dataclass
class Verdict:
    conclusion: Conclusion
    holds: bool
    summary: str
    trace: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        head = f"{'YES' if self.holds else 'NO '} | {self.summary}"
        if self.trace:
            return head + "\n" + "\n".join(self.trace)
        return head


class Reasoner:
    def __init__(self, theory: Theory) -> None:
        self.theory = theory
        self.ext: Extension = extension(theory)

    @classmethod
    def from_ddl(cls, source: str) -> "Reasoner":
        return cls(parse(source))

    @classmethod
    def from_json(cls, data) -> "Reasoner":
        return cls(theory_from_json(data))

    def with_facts(self, facts: set[Literal]) -> "Reasoner":
        """A fresh reasoner with extra case facts (for what-if / appeal flows)."""
        return Reasoner(self.theory.with_facts(facts))

    # ------------------------------------------------------------- querying
    def holds(self, query: str | Conclusion) -> bool:
        return self.query(query).holds

    def query(self, query: str | Conclusion, trace: bool = True) -> Verdict:
        c = query if isinstance(query, Conclusion) else parse_query(query)
        in_base = c.modality == "⊥" or c.literal.atom in self.theory.herbrand_atoms()
        if in_base:
            ok = c in self.ext.proven
        else:
            pos = _VACUOUS_POS[c.modality]
            ok = pos if c.positive else (not pos)
        positive_form = Conclusion("+", c.modality, c.literal)
        summary = describe_conclusion(positive_form)
        lines = self._trace(c) if (trace and ok and in_base) else []
        return Verdict(c, ok, summary, lines)

    def _elem_conclusion(self, b: BodyElem) -> Conclusion:
        if isinstance(b, ModalLiteral):
            return Conclusion("-" if b.negated else "+", b.op, b.lit)
        if is_bottom(b):
            return Conclusion("+", "⊥", BOTTOM)
        return Conclusion("+", "C", b)

    def _trace(self, c: Conclusion, visited=None, indent=0) -> list[str]:
        visited = visited if visited is not None else set()
        pad = "  " * indent
        j = self.ext.proven.get(c)
        if j is None:
            return [f"{pad}- {describe_conclusion(c)} (not derived)"]
        head = f"{pad}- {describe_conclusion(c)}  [{j.kind}"
        head += f" via {j.applied}]" if j.applied else "]"
        out = [head]
        for label, why in j.defeated:
            out.append(f"{pad}    (counter {label}: {why})")
        if c in visited or not j.applied:
            return out
        visited = visited | {c}
        try:
            rule = self.theory.rule(j.applied)
        except KeyError:
            return out
        for b in rule.body:
            out += self._trace(self._elem_conclusion(b), visited, indent + 1)
        return out

    # ------------------------------------------------------------- reporting
    _ORDER = {"O": 0, "Ps": 1, "P": 2, "Pw": 3, "⊥": 4, "C": 5}
    _CONCISE = {"O", "Ps", "⊥", "C"}

    def conclusions(self, concise: bool = True) -> list[Conclusion]:
        """Positively derived conclusions, deontic effects first. By default
        omits weak/generic permission (the mere absence of a prohibition), which
        holds for almost every literal; pass ``concise=False`` for everything."""
        pos = set(self.ext.conclusions("+"))
        if concise:
            pos = {c for c in pos if c.modality in self._CONCISE}
        return sorted(
            pos, key=lambda c: (self._ORDER.get(c.modality, 9), str(c.literal))
        )

    def report(self, concise: bool = True) -> str:
        lines = ["= Theory =", describe_theory(self.theory), "", "= Conclusions ="]
        for c in self.conclusions(concise=concise):
            lines.append(f"  {c}\t{describe_conclusion(c)}")
        return "\n".join(lines)


def reason(source: str) -> Reasoner:
    """Convenience: build a Reasoner from DSL text."""
    return Reasoner.from_ddl(source)
