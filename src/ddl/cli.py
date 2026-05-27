"""Command-line interface.

    ddl run    THEORY [--facts "a. -b."]      # compute and report all verdicts
    ddl query  THEORY QUERY [--facts ...]      # one tagged-literal verdict + trace
    ddl render THEORY                          # theory back in natural language

THEORY is a .ddl file, or a .json file (or pass --json) using the structured
LLM-facing format.
"""

from __future__ import annotations

import argparse
import sys

from .api import Reasoner
from .json_io import theory_from_json
from .parser import ParseError, parse
from .render import describe_theory
from .syntax import Theory


def _load(path: str, as_json: bool) -> Theory:
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    if as_json or path.endswith(".json"):
        return theory_from_json(text)
    return parse(text)


def _add_facts(theory: Theory, facts: str | None) -> Theory:
    if not facts:
        return theory
    extra = parse(facts).facts
    return theory.with_facts(extra)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ddl", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    for name in ("run", "query", "render"):
        p = sub.add_parser(name)
        p.add_argument("theory")
        if name == "query":
            p.add_argument("query")
            p.add_argument("--no-trace", action="store_true")
        if name in ("run", "query"):
            p.add_argument("--facts", default=None, help='extra facts, e.g. "a. -b."')
        if name == "run":
            p.add_argument(
                "--all", action="store_true",
                help="show every conclusion, incl. weak/generic permission",
            )
        p.add_argument("--json", action="store_true", help="parse theory as JSON")

    args = ap.parse_args(argv)
    try:
        theory = _load(args.theory, getattr(args, "json", False))
        if getattr(args, "facts", None):
            theory = _add_facts(theory, args.facts)
    except (ParseError, OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.cmd == "render":
        print(describe_theory(theory))
        return 0

    reasoner = Reasoner(theory)
    if args.cmd == "run":
        print(reasoner.report(concise=not args.all))
        return 0

    # query
    verdict = reasoner.query(args.query, trace=not args.no_trace)
    print(verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
