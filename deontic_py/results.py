"""Typed results parsed from the reasoner's ``--json`` output.

Every dataclass here mirrors one JSON renderer in ``Deontic/Pretty.lean`` — that
file is the source of truth for the field names. Construct them with the
``from_json`` classmethods; callers normally get them back from
:class:`deontic_py.client.Deontic`, not by hand.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# The four reserved keys in the flat object emitted by `renderExtensionJSON`;
# every *other* key is an atom name.
_META_KEYS = frozenset(
    {"hasViolation", "violatingRules", "hasUnresolvedConflicts", "unresolvedConflicts"}
)

# Status string -> 4-class verdict (lifted from caselaw/engine.py so that wrapper
# can collapse to a one-liner). `fact`/`unknown` fall through to the default.
_STATUS_TO_VERDICT = {
    "F": "forbidden",
    "O": "obligatory",
    "Ps": "allowed",
    "P": "allowed",
    "Pw": "allowed",
    "unresolved": "dilemma",
}


def status_code(status: str) -> str:
    """Leading token of a normative status string.

    ``"O(use)" -> "O"``, ``"fact(license)" -> "fact"``, ``"unresolved" ->
    "unresolved"``. Mirrors how `Query.lean` formats statuses (``MOD(atom)`` or a
    bare word).
    """
    return status.split("(", 1)[0].strip()


def status_to_verdict(status: str) -> str:
    """Map a normative status to ``forbidden|obligatory|allowed|dilemma``.

    Anything not explicitly forbidden/obligatory/conflicted is ``allowed`` (weak
    permission = "nothing forbids it"), matching the project's 4-class scheme.
    """
    return _STATUS_TO_VERDICT.get(status_code(status), "allowed")


@dataclass(frozen=True)
class Tag:
    """One tagged literal (``renderTagJSON``): a ``+∂`` derivation entry."""

    positive: bool
    modality: str  # C, O, P, Pw, Ps
    bearer: str | None
    literal: str  # e.g. "use" or "~publish"

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> "Tag":
        return cls(
            positive=d["positive"],
            modality=d["modality"],
            bearer=d.get("bearer"),
            literal=d["literal"],
        )


@dataclass(frozen=True)
class AtomStatus:
    """An atom's normative status plus its supporting tags (``renderAtomJSON``)."""

    atom: str
    status: str  # raw, e.g. "O(use)" / "unresolved" / "fact(license)"
    tags: list[Tag] = field(default_factory=list)

    @property
    def code(self) -> str:
        """Leading modality token of :attr:`status` (``"O(use)" -> "O"``)."""
        return status_code(self.status)

    @property
    def verdict(self) -> str:
        """4-class verdict for this atom (``forbidden|obligatory|allowed|dilemma``)."""
        return status_to_verdict(self.status)

    @classmethod
    def from_json(cls, atom: str, d: dict[str, Any]) -> "AtomStatus":
        return cls(
            atom=atom,
            status=d["status"],
            tags=[Tag.from_json(t) for t in d.get("tags", [])],
        )


@dataclass(frozen=True)
class Conflict:
    """An unresolved obligation deadlock on one atom (``renderConflictJSON``)."""

    atom: str
    for_o: list[str]  # rule labels supporting O(atom)
    against_o: list[str]  # rule labels supporting O(~atom)
    unresolved_pairs: list[tuple[str, str]]  # (r, s) with no superiority either way

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> "Conflict":
        return cls(
            atom=d["atom"],
            for_o=list(d.get("forO", [])),
            against_o=list(d.get("againstO", [])),
            unresolved_pairs=[tuple(p) for p in d.get("unresolvedPairs", [])],
        )


@dataclass(frozen=True)
class Extension:
    """Full result of ``check`` / ``query`` (``renderExtensionJSON``).

    ``atoms`` is keyed by atom name; the four meta-fields carry the global
    violation / conflict signals. ``check`` covers the whole Herbrand base;
    ``query`` covers only the queried atoms but is the *same* shape.
    """

    atoms: dict[str, AtomStatus]
    has_violation: bool
    violating_rules: list[str]
    has_unresolved_conflicts: bool
    unresolved_conflicts: list[Conflict]

    def __getitem__(self, atom: str) -> AtomStatus:
        return self.atoms[atom]

    def __contains__(self, atom: str) -> bool:
        return atom in self.atoms

    def status(self, atom: str) -> str:
        """Raw status string for ``atom`` (``"unknown"`` if absent)."""
        a = self.atoms.get(atom)
        return a.status if a else "unknown"

    def code(self, atom: str) -> str:
        """Leading status token for ``atom`` (``"unknown"`` if absent)."""
        return status_code(self.status(atom))

    def verdict(self, atom: str) -> str:
        """4-class verdict for ``atom``."""
        return status_to_verdict(self.status(atom))

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> "Extension":
        atoms = {
            name: AtomStatus.from_json(name, val)
            for name, val in d.items()
            if name not in _META_KEYS
        }
        return cls(
            atoms=atoms,
            has_violation=d.get("hasViolation", False),
            violating_rules=list(d.get("violatingRules", [])),
            has_unresolved_conflicts=d.get("hasUnresolvedConflicts", False),
            unresolved_conflicts=[
                Conflict.from_json(c) for c in d.get("unresolvedConflicts", [])
            ],
        )


# `query` and `check` share the renderer, so they share the dataclass.
QueryResult = Extension


@dataclass(frozen=True)
class WhyRule:
    """One applicable rule in a why-report (``renderWhyEntryJSON``):
    its label, its full one-line text, and the labels of the applicable
    counter-rules that defeat it by superiority."""

    rule: str
    text: str
    defeated_by: list[str]

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> "WhyRule":
        return cls(
            rule=d["rule"],
            text=d.get("text", ""),
            defeated_by=list(d.get("defeatedBy", [])),
        )


@dataclass(frozen=True)
class WhyReport:
    """Proof certificate for one atom in one bearer slice
    (``renderWhyReportJSON``): the status plus the *applicable* prescriptive
    rules concluding the atom (``for_o``) and its complement (``against_o``).
    Inapplicable rules are omitted — they played no part."""

    atom: str
    bearer: str
    status: str
    for_o: list[WhyRule]
    against_o: list[WhyRule]

    @property
    def winning_rules(self) -> list[str]:
        """Labels of the undefeated applicable rules on the derived side
        (``O(...)`` -> for_o, ``F(...)`` -> against_o; else empty)."""
        side = {"O": self.for_o, "F": self.against_o}.get(status_code(self.status))
        return [r.rule for r in side if not r.defeated_by] if side else []

    @classmethod
    def from_json(cls, atom: str, bearer: str, d: dict[str, Any]) -> "WhyReport":
        return cls(
            atom=atom,
            bearer=bearer,
            status=d["status"],
            for_o=[WhyRule.from_json(r) for r in d.get("forO", [])],
            against_o=[WhyRule.from_json(r) for r in d.get("againstO", [])],
        )


@dataclass(frozen=True)
class AbduceResult:
    """Backward search result (``renderAbduceResultJSON``).

    ``minimal_configs`` are the subset-minimal fact configurations (each a list
    of literal strings) that make the goal hold.
    """

    goal: list[str]
    assumed_facts: list[str]
    minimal_configs: list[list[str]]
    minimal_count: int
    satisfying: int
    evaluated: int
    truncated: bool

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> "AbduceResult":
        return cls(
            goal=list(d.get("goal", [])),
            assumed_facts=list(d.get("assumedFacts", [])),
            minimal_configs=[list(c) for c in d.get("minimalConfigs", [])],
            minimal_count=d.get("minimalCount", 0),
            satisfying=d.get("satisfying", 0),
            evaluated=d.get("evaluated", 0),
            truncated=d.get("truncated", False),
        )


@dataclass(frozen=True)
class Provenance:
    """An atom's source pointer (at least one of ``quote`` / ``uri`` is set)."""

    quote: str | None
    uri: str | None

    @classmethod
    def from_json(cls, d: dict[str, Any] | None) -> "Provenance | None":
        if not d:
            return None
        return cls(quote=d.get("quote"), uri=d.get("uri"))


@dataclass(frozen=True)
class AtomEntry:
    """One atom's grounding from ``atoms`` (``renderAtomsJSON``)."""

    atom: str
    description: str | None
    provenance: Provenance | None
    resolved: str | None  # provenance text inlined when --resolve hit a local file

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> "AtomEntry":
        return cls(
            atom=d["atom"],
            description=d.get("description"),
            provenance=Provenance.from_json(d.get("provenance")),
            resolved=d.get("resolved"),
        )
