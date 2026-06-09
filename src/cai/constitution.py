"""Load constitutional principles and sample them for critique-revision."""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

import yaml

from .config import resolve_path


@dataclass
class Principle:
    name: str
    critique_request: str
    revision_request: str


@dataclass
class Constitution:
    principles: list[Principle]
    judge_rubric: str

    def sample(self, rng: random.Random | None = None) -> Principle:
        return (rng or random).choice(self.principles)


def load_constitution(path: str | Path) -> Constitution:
    data = yaml.safe_load(resolve_path(path).read_text())
    principles = [
        Principle(
            name=p["name"],
            critique_request=" ".join(p["critique_request"].split()),
            revision_request=" ".join(p["revision_request"].split()),
        )
        for p in data["principles"]
    ]
    if not principles:
        raise ValueError("Constitution has no principles")
    rubric = " ".join((data.get("judge_rubric") or "").split())
    return Constitution(principles=principles, judge_rubric=rubric)
