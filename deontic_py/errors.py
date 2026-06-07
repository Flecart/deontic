"""Exceptions raised by :mod:`deontic_py`."""
from __future__ import annotations


class DeonticError(Exception):
    """Base class for every error this package raises."""


class DeonticNotBuilt(DeonticError):
    """The `deontic` binary could not be located or is not executable.

    Carries the build hint so callers (and LLMs) get an actionable message.
    """


class DeonticParseError(DeonticError):
    """The reasoner rejected the input.

    Covers the two `IO.Process.exit 1` paths in `Main.lean`: a `.ddl` parse
    error and an atom used without a (mandatory) description, plus bad
    goal/assumption tokens. The reasoner's stderr is preserved verbatim.
    """


class DeonticTimeout(DeonticError):
    """The reasoner did not finish within the configured timeout."""
