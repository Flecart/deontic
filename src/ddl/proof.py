"""Proof tags, conclusions, and justification records.

A conclusion is a tagged literal ``+/-d_X l`` where X is a modality
(C, O, P, Pw, Ps) and l a plain literal, following Governatori (2018) pp.17-21.
Prohibition is read off the obligation tag: ``+dO ~l`` means ``Fl``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .syntax import Literal

Modality = str  # one of: C, O, P, Pw, Ps
Sign = str  # '+' or '-'

MODALITIES = ("C", "O", "P", "Pw", "Ps")


@dataclass(frozen=True)
class Conclusion:
    """A tagged literal, e.g. +dC(complaint) or +dO(-publish) meaning F publish."""

    sign: Sign  # '+' (provable) or '-' (refuted)
    modality: Modality
    literal: Literal

    def __str__(self) -> str:
        return f"{self.sign}d{self.modality} {self.literal}"

    @property
    def positive(self) -> bool:
        return self.sign == "+"


@dataclass
class Justification:
    """Why a conclusion holds, for traceability.

    ``kind`` is a short reason code; ``applied`` is the supporting rule label (if
    any); ``defeated`` lists (counter-rule, why-it-failed); ``detail`` is free
    text for the human/LLM-facing trace.
    """

    conclusion: Conclusion
    kind: str
    applied: str | None = None
    defeated: list[tuple[str, str]] = field(default_factory=list)
    detail: str = ""

    def __str__(self) -> str:
        parts = [f"{self.conclusion}  [{self.kind}]"]
        if self.applied:
            parts.append(f"by {self.applied}")
        for label, why in self.defeated:
            parts.append(f"counter {label}: {why}")
        if self.detail:
            parts.append(self.detail)
        return "  ".join(parts)
