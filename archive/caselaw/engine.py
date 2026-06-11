"""Thin wrapper around the `deontic` binary for the case-law experiment.

A *case* is a frozenset of true fact-atoms (everything else is false/absent).
A *verdict* on a target atom is its modal status under a DDL theory + those facts:
  F -> "forbidden", O -> "obligatory", Ps/P -> "permitted", else "unregulated".
We also expose conflict detection ([JUDGE] = an unresolved deontic conflict).
"""
from __future__ import annotations

import os
import re
import subprocess
import tempfile
from functools import lru_cache

BIN = os.environ.get("DEONTIC_BIN",
                     os.path.expanduser("~/Desktop/work/deontic/.lake/build/bin/deontic"))

# 4-class verdict scheme: anything not forbidden/obligatory/conflicted is "allowed"
# (weak permission = "nothing forbids it"), so an empty corpus defaults to allowed.
VERDICTS = ("forbidden", "obligatory", "allowed", "dilemma")
_STATUS_TO_VERDICT = {"F": "forbidden", "O": "obligatory",
                      "Ps": "allowed", "P": "allowed", "Pw": "allowed",
                      "unresolved": "dilemma"}


def _write(theory: str, facts) -> str:
    body = f"facts: {', '.join(sorted(facts))}\n\n{theory}"
    fd, path = tempfile.mkstemp(suffix=".ddl")
    with os.fdopen(fd, "w") as fh:
        fh.write(body)
    return path


def _run(args: list[str]) -> str:
    try:
        p = subprocess.run([BIN, *args], capture_output=True, text=True, timeout=30)
        return p.stdout + p.stderr
    except Exception as exc:  # noqa
        return f"__ERROR__ {type(exc).__name__}: {exc}"


@lru_cache(maxsize=200_000)
def _status_cached(theory: str, facts: frozenset, atom: str) -> str:
    path = _write(theory, facts)
    try:
        out = _run(["query", path, atom])
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    if out.startswith("__ERROR__"):
        return "ERROR"
    if "unresolved obligation conflict" in out or re.search(
            rf"\b{re.escape(atom)}\s*:\s*unresolved", out):
        return "unresolved"
    for line in out.splitlines():
        if re.search(rf"\b{re.escape(atom)}\s*:", line) and "(" in line:
            verdict = line.split(":", 1)[1].strip()        # "F(act)"
            return verdict.split("(", 1)[0].strip()         # "F"
    return "unknown"


def status(theory: str, facts, atom: str) -> str:
    return _status_cached(theory, frozenset(facts), atom)


def verdict(theory: str, facts, atom: str) -> str:
    """Map modal status of `atom` to a verdict label (default: allowed)."""
    return _STATUS_TO_VERDICT.get(status(theory, facts, atom), "allowed")


@lru_cache(maxsize=200_000)
def _check_cached(theory: str, facts: frozenset) -> str:
    path = _write(theory, facts)
    try:
        out = _run(["check", path])
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
    return out


def has_unresolved_conflict(theory: str, facts, atom: str) -> bool:
    """A genuine deontic dilemma on `atom`: neither the act nor its negation is
    definitely obligatory/forbidden, yet both are 'attempted' (both +∂ proofs
    blocked by the other). We approximate with the engine's JUDGE/conflict signal
    or a both-directions ambiguity on the atom."""
    # Only a genuine *unresolved obligation conflict* counts as a dilemma.
    # (A "non-compensable violation" is just an unmet obligation — normal.)
    return status(theory, facts, atom) == "unresolved"
