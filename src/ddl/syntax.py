"""Abstract syntax for Defeasible Deontic Logic theories.

Follows Governatori (2018), "Practical Normative Reasoning with Defeasible
Deontic Logic". A theory is D = (F, R^C, R^O, <) where F is a set of plain
literals (facts), R^C constitutive rules, R^O prescriptive rules, and < the
superiority relation.

Design note on the superiority relation: the paper's worked examples are only
consistent if ``r < s`` means *s is superior* (s defeats r). The prose on p.10
reads the other way, but every example (e.g. ``r0 < r1`` lets a license enable
use) requires the "s wins" reading. We adopt that and store ordered pairs
``(weaker, stronger)``; see ``Theory.beats``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal as TypingLiteral

# Deontic operators. Prohibition F is represented via O of the complement
# (F l == O ~l, eq. 3), so it is not a stored operator.
DeonticOp = TypingLiteral["O", "P", "Pw", "Ps"]
RuleMode = TypingLiteral["C", "O"]
RuleStrength = TypingLiteral["defeasible", "defeater"]


@dataclass(frozen=True)
class Literal:
    """A plain literal: an atom or its negation."""

    atom: str
    negated: bool = False

    @property
    def complement(self) -> "Literal":
        return Literal(self.atom, not self.negated)

    def __str__(self) -> str:
        return f"-{self.atom}" if self.negated else self.atom


@dataclass(frozen=True)
class ModalLiteral:
    """A deontic literal: a deontic operator applied to a plain literal.

    ``negated`` marks the negation of the whole modal literal (e.g. ``-Op``).
    Prohibition ``Fp`` is encoded as ``ModalLiteral('O', ~p)``.
    """

    op: DeonticOp
    lit: Literal
    negated: bool = False

    def __str__(self) -> str:
        prefix = "-" if self.negated else ""
        return f"{prefix}{self.op}{self.lit}"


# A rule body element is either a plain literal (a brute fact condition) or a
# modal literal (a normative condition that must itself be derived).
BodyElem = Literal | ModalLiteral


@dataclass(frozen=True)
class Rule:
    """A defeasible rule or defeater.

    ``mode`` distinguishes constitutive ('C', counts-as -> plain conclusion) from
    prescriptive ('O', -> obligation). ``head`` is the consequent as an ordered
    tuple of plain literals: a singleton for constitutive rules, or a
    compensation (otimes) chain for prescriptive rules, where head[0] is the
    primary obligation and later elements are contrary-to-duty compensations.
    """

    label: str
    mode: RuleMode
    strength: RuleStrength
    body: tuple[BodyElem, ...]
    head: tuple[Literal, ...]
    gloss: str = ""  # the natural-language source of the norm, if known

    @property
    def is_defeater(self) -> bool:
        return self.strength == "defeater"

    @property
    def primary(self) -> Literal:
        return self.head[0]

    def __str__(self) -> str:
        arrow = "~>" if self.is_defeater else "=>"
        body = ", ".join(str(b) for b in self.body)
        head = " (x) ".join(str(h) for h in self.head)
        return f"{self.label}: {body} {arrow}{self.mode} {head}"


@dataclass
class Theory:
    """A defeasible deontic theory D = (F, R^C, R^O, <)."""

    facts: set[Literal] = field(default_factory=set)
    rules: list[Rule] = field(default_factory=list)
    # superiority stored as (weaker, stronger) label pairs: weaker < stronger.
    superiority: set[tuple[str, str]] = field(default_factory=set)

    def beats(self, stronger: str, weaker: str) -> bool:
        """True if rule ``stronger`` is superior to rule ``weaker``."""
        return (weaker, stronger) in self.superiority

    @property
    def constitutive(self) -> list[Rule]:
        return [r for r in self.rules if r.mode == "C"]

    @property
    def prescriptive(self) -> list[Rule]:
        return [r for r in self.rules if r.mode == "O"]

    def rule(self, label: str) -> Rule:
        for r in self.rules:
            if r.label == label:
                return r
        raise KeyError(label)

    def add_fact(self, lit: Literal) -> None:
        self.facts.add(lit)

    def with_facts(self, extra: set[Literal]) -> "Theory":
        """Return a shallow copy with additional facts (for what-if queries)."""
        return Theory(
            facts=self.facts | extra,
            rules=list(self.rules),
            superiority=set(self.superiority),
        )

    def herbrand_atoms(self) -> set[str]:
        atoms: set[str] = set()
        for f in self.facts:
            atoms.add(f.atom)
        for r in self.rules:
            for b in r.body:
                atoms.add(b.lit.atom if isinstance(b, ModalLiteral) else b.atom)
            for h in r.head:
                atoms.add(h.atom)
        return atoms


def lit(atom: str, negated: bool = False) -> Literal:
    return Literal(atom, negated)


# The distinguished literal for a non-compensable violation (Governatori 2018,
# p.20-21). It carries the +d_bottom proof tag and may only appear in rule
# antecedents.
BOTTOM_ATOM = "⊥"  # the symbol bottom
BOTTOM = Literal(BOTTOM_ATOM)


def is_bottom(l: Literal) -> bool:
    return isinstance(l, Literal) and l.atom == BOTTOM_ATOM


def normalize_chain(head: tuple[Literal, ...]) -> tuple[Literal, ...]:
    """Apply otimes duplication/contraction (sect. 3.2): keep the leftmost
    occurrence of each literal, dropping later duplicates."""
    seen: set[Literal] = set()
    out: list[Literal] = []
    for h in head:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return tuple(out)
