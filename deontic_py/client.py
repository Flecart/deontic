"""A typed, JSON-backed Python client for the ``deontic`` reasoner.

This is the single supported way to drive the engine from Python. Every method
runs the CLI with ``--json`` and parses the structured output into the
dataclasses in :mod:`deontic_py.results` — no text scraping.

    from deontic_py import Deontic
    d = Deontic()
    ext = d.check("examples/ex1_license.ddl")
    ext.verdict("use")            # -> "obligatory"
    d.query(ddl_string, ["publish"])["publish"].status
    d.abduce(ddl, ["P(publish)"], all=True).minimal_configs

A theory is supplied as raw ``.ddl`` text *or* a path; a path is detected and
passed straight through, otherwise the text is written to a temp file that is
removed afterwards.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

from .errors import DeonticNotBuilt, DeonticParseError, DeonticTimeout
from .results import (
    AbduceResult,
    AtomEntry,
    Extension,
    QueryResult,
    WhyReport,
    status_code,
    status_to_verdict,
)

_BUILD_HINT = 'export PATH="$HOME/.elan/bin:$PATH" && lake build deontic'
# stderr substrings that mean "bad input" rather than "engine crashed".
_PARSE_MARKERS = ("Parse error", "used without a description",
                  "Assumption error", "Goal error", "import")


def _find_repo_root(start: Path) -> Path | None:
    """Walk up from ``start`` looking for the dir containing ``lakefile.lean``."""
    for parent in [start, *start.parents]:
        if (parent / "lakefile.lean").exists():
            return parent
    return None


def _is_runnable(path: str) -> bool:
    return os.path.isfile(path) and os.access(path, os.X_OK)


def _resolve_binary(binary: str | os.PathLike | None) -> str:
    """Locate the ``deontic`` executable.

    An explicit ``binary`` argument is authoritative — if it is given but not a
    runnable file, that is an error (no silent fallback). Otherwise auto-detect:
    ``$DEONTIC_BIN`` → ``<repo>/.lake/build/bin/deontic`` (repo found by walking
    up from this file). Raises :class:`DeonticNotBuilt` with the build hint when
    nothing usable is found.
    """
    if binary:
        path = str(binary)
        if _is_runnable(path):
            return path
        raise DeonticNotBuilt(
            f"deontic binary '{path}' is missing or not executable.\n"
            f"  build it with:  {_BUILD_HINT}"
        )

    candidates: list[str] = []
    env = os.environ.get("DEONTIC_BIN")
    if env:
        candidates.append(env)
    root = _find_repo_root(Path(__file__).resolve().parent)
    if root:
        candidates.append(str(root / ".lake" / "build" / "bin" / "deontic"))

    for c in candidates:
        if _is_runnable(c):
            return c
    looked = ", ".join(candidates) or "(no candidates)"
    raise DeonticNotBuilt(
        f"deontic binary not found (tried: {looked}). "
        f"Set $DEONTIC_BIN or build it:\n  {_BUILD_HINT}"
    )


def _extract_json(stdout: str):
    """Parse the first JSON value in ``stdout``, ignoring any trailing text.

    Necessary because ``query --json`` appends human-readable warnings after the
    JSON object (the warning block in ``Main.lean`` isn't gated on ``--json`` for
    the query branch). ``raw_decode`` from the first ``{``/``[`` handles this and
    leaves ``check``/``abduce``/``atoms`` (already clean) unaffected.
    """
    start = min(
        (i for i in (stdout.find("{"), stdout.find("[")) if i != -1),
        default=-1,
    )
    if start == -1:
        raise DeonticParseError(f"no JSON found in reasoner output:\n{stdout}")
    try:
        obj, _ = json.JSONDecoder().raw_decode(stdout, start)
    except json.JSONDecodeError as exc:
        raise DeonticParseError(
            f"could not parse reasoner JSON ({exc}):\n{stdout}"
        ) from exc
    return obj


class Deontic:
    """Driver for the ``deontic`` CLI.

    Parameters
    ----------
    binary:
        Path to the executable. Defaults to ``$DEONTIC_BIN`` then the repo build.
    timeout:
        Per-call wall-clock limit in seconds (default 30).
    cache:
        If true, memoise raw command output keyed on the full argument vector —
        useful for the large fact-sweep experiments (replaces the per-harness
        ``@lru_cache`` pattern).
    """

    def __init__(
        self,
        binary: str | os.PathLike | None = None,
        *,
        timeout: float = 30.0,
        cache: bool = False,
    ) -> None:
        self.binary = _resolve_binary(binary)
        self.timeout = timeout
        self._cache: dict[tuple, str] | None = {} if cache else None

    # ── raw command plumbing ────────────────────────────────────────────────

    def _run(self, command: str, theory: str | os.PathLike, args: list[str]) -> str:
        """Run ``deontic <command> <file> <args>`` and return raw stdout.

        ``theory`` may be a path to an existing ``.ddl`` file or raw DDL text.
        """
        path, tmp = self._theory_path(theory)
        try:
            argv = [self.binary, command, path, *args]
            key = tuple(argv[1:]) if self._cache is not None else None
            if key is not None and key in self._cache:
                return self._cache[key]
            try:
                proc = subprocess.run(
                    argv, capture_output=True, text=True, timeout=self.timeout
                )
            except subprocess.TimeoutExpired as exc:
                raise DeonticTimeout(
                    f"deontic {command} timed out after {self.timeout}s"
                ) from exc
            if proc.returncode != 0:
                err = (proc.stderr or proc.stdout or "").strip()
                if any(m in err for m in _PARSE_MARKERS):
                    raise DeonticParseError(err)
                raise DeonticParseError(
                    f"deontic {command} exited {proc.returncode}: {err}"
                )
            out = proc.stdout
            if key is not None:
                self._cache[key] = out  # type: ignore[index]
            return out
        finally:
            if tmp is not None:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass

    @staticmethod
    def _theory_path(theory: str | os.PathLike) -> tuple[str, str | None]:
        """Return ``(path, tmp_path_to_clean_or_None)`` for a theory argument.

        A ``Path``, or a ``str`` naming an existing file, is used in place;
        anything else is treated as DDL source and written to a temp file.
        """
        if isinstance(theory, os.PathLike):
            return os.fspath(theory), None
        if isinstance(theory, str) and "\n" not in theory and os.path.isfile(theory):
            return theory, None
        fd, tmp = tempfile.mkstemp(suffix=".ddl")
        with os.fdopen(fd, "w") as fh:
            fh.write(theory)
        return tmp, tmp

    @staticmethod
    def _assume_args(assume: list[str] | None) -> list[str]:
        if not assume:
            return []
        return ["--assume", ",".join(assume)]

    # ── commands ────────────────────────────────────────────────────────────

    def check(
        self, theory: str | os.PathLike, *, assume: list[str] | None = None
    ) -> Extension:
        """Compute the full extension of ``theory`` (every Herbrand-base atom)."""
        out = self._run("check", theory, ["--json", *self._assume_args(assume)])
        return Extension.from_json(_extract_json(out))

    def query(
        self,
        theory: str | os.PathLike,
        atoms: list[str] | None = None,
        *,
        assume: list[str] | None = None,
    ) -> QueryResult:
        """Normative status of ``atoms`` (or the whole base if ``atoms`` is None)."""
        args = [*(atoms or []), "--json", *self._assume_args(assume)]
        out = self._run("query", theory, args)
        return Extension.from_json(_extract_json(out))

    def abduce(
        self,
        theory: str | os.PathLike,
        goals: list[str],
        *,
        all: bool = False,
        limit: int | None = None,
        assume: list[str] | None = None,
    ) -> AbduceResult:
        """Fact configurations that make ``goals`` hold (backward search).

        Goal tokens use the CLI syntax, e.g. ``"P(Disclose)"``, ``"O(use)"``,
        ``"!C(Notify)"`` (``!`` = must NOT hold). The JSON result already lists
        every minimal configuration; ``all`` is accepted for parity with the CLI
        (where it only controls how many are *printed*) and is otherwise inert.
        """
        args = [*goals, "--json", *self._assume_args(assume)]
        if all:
            args.append("--all")
        if limit is not None:
            args += ["--limit", str(limit)]
        out = self._run("abduce", theory, args)
        return AbduceResult.from_json(_extract_json(out))

    def why(
        self,
        theory: str | os.PathLike,
        atoms: list[str],
        *,
        bearer: str | None = None,
        assume: list[str] | None = None,
    ) -> dict[str, dict[str, WhyReport]]:
        """Proof certificates for ``atoms`` (``query --why --json``).

        Returns ``{atom: {bearer_label: WhyReport}}`` — for each atom, the
        applicable rules on each side of the obligation question with
        superiority-defeat annotations. ``bearer_label`` is the party name or
        ``"(unattributed)"``.
        """
        args = [*atoms, "--why", "--json", *self._assume_args(assume)]
        if bearer:
            args += ["--bearer", bearer]
        out = self._run("query", theory, args)
        raw = _extract_json(out)
        return {
            atom: {
                b: WhyReport.from_json(atom, b, rep)
                for b, rep in entry.get("byBearer", {}).items()
            }
            for atom, entry in raw.items()
        }

    def atoms(
        self, theory: str | os.PathLike, *, resolve: bool = False
    ) -> list[AtomEntry]:
        """The atom dictionary: each atom's description and provenance.

        ``resolve=True`` inlines provenance text for atoms whose URI points at a
        local markdown file. (Runs the non-enforcing load, so it works even on
        theories with undescribed atoms.)
        """
        args = ["--json"]
        if resolve:
            args.append("--resolve")
        out = self._run("atoms", theory, args)
        return [AtomEntry.from_json(e) for e in _extract_json(out)]

    # ── convenience (folds in caselaw/engine.py) ────────────────────────────

    def status(
        self, theory: str | os.PathLike, atom: str, *, assume: list[str] | None = None
    ) -> str:
        """Leading status token for one ``atom``: ``O|F|Ps|P|Pw|fact|unresolved|unknown``."""
        res = self.query(theory, [atom], assume=assume)
        return status_code(res.status(atom))

    def verdict(
        self, theory: str | os.PathLike, atom: str, *, assume: list[str] | None = None
    ) -> str:
        """4-class verdict for one ``atom``: ``forbidden|obligatory|allowed|dilemma``."""
        res = self.query(theory, [atom], assume=assume)
        return status_to_verdict(res.status(atom))
