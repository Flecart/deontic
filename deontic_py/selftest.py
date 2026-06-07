"""End-to-end self-test: run with ``python -m deontic_py.selftest``.

Drives the real binary on real theories and asserts the typed client agrees with
the CLI's own ``--json`` output. Exits non-zero on any failure.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from . import (
    Deontic,
    DeonticNotBuilt,
    DeonticParseError,
    TOOL_SCHEMA,
    dispatch,
    status_to_verdict,
)

REPO = Path(__file__).resolve().parent.parent
EX1 = REPO / "examples" / "ex1_license.ddl"

# A tiny theory that triggers a non-compensable violation: pay is obligated by
# the fact `breach` but is absent from the facts -> +∂_⊥.
VIOLATION_DDL = """\
facts: breach
atom breach: a breach occurred
atom pay: the penalty is paid
r: breach =>O pay
"""

PASSED = 0


def check(label: str, cond: bool) -> None:
    global PASSED
    if not cond:
        raise AssertionError(f"FAIL: {label}")
    PASSED += 1
    print(f"  ok: {label}")


def cli_json(d: Deontic, *argv: str):
    """Run the raw CLI and json-decode its (first) output value, for cross-check."""
    proc = subprocess.run(
        [d.binary, *argv], capture_output=True, text=True, timeout=30
    )
    out = proc.stdout
    start = min((i for i in (out.find("{"), out.find("[")) if i != -1), default=-1)
    obj, _ = json.JSONDecoder().raw_decode(out, start)
    return obj


def main() -> int:
    d = Deontic()
    print(f"binary: {d.binary}")

    print("[check]")
    ext = d.check(EX1)
    check("use is obligatory", ext.verdict("use") == "obligatory")
    check("publish is a dilemma", ext.verdict("publish") == "dilemma")
    check("has an unresolved conflict", ext.has_unresolved_conflicts)
    check("conflict names publish", ext.unresolved_conflicts[0].atom == "publish")
    check("no violation on the base facts", not ext.has_violation)
    # cross-check against the CLI's own JSON
    raw = cli_json(d, "check", str(EX1), "--json")
    check("check matches CLI json (use)",
          ext["use"].status == raw["use"]["status"])
    check("tag bearer parsed", any(t.bearer == "Licensee" for t in ext["use"].tags))

    print("[query]  (note: query --json emits trailing prose; parser must cope)")
    q = d.query(EX1, ["publish", "use"])
    check("query use == check use", q["use"].status == ext["use"].status)
    check("query publish unresolved", q["publish"].code == "unresolved")
    rawq = cli_json(d, "query", str(EX1), "publish", "use", "--json")
    check("query matches CLI json (publish)",
          q["publish"].status == rawq["publish"]["status"])

    print("[status/verdict convenience]")
    check("status(use) == O", d.status(EX1, "use") == "O")
    check("verdict(use) == obligatory", d.verdict(EX1, "use") == "obligatory")
    check("verdict(publish) == dilemma", d.verdict(EX1, "publish") == "dilemma")
    check("status_to_verdict(F(x)) == forbidden",
          status_to_verdict("F(x)") == "forbidden")

    print("[abduce]")
    ab = d.abduce(EX1, ["P(publish)"], all=True)
    configs = sorted(tuple(c) for c in ab.minimal_configs)
    check("abduce P(publish) -> {approval},{commission}",
          configs == [("approval",), ("commission",)])
    rawa = cli_json(d, "abduce", str(EX1), "P(publish)", "--all", "--json")
    check("abduce matches CLI json count",
          ab.minimal_count == rawa["minimalCount"])

    print("[atoms]")
    entries = d.atoms(EX1)
    check("atoms returns the whole dictionary", len(entries) == 8)
    by_name = {e.atom: e for e in entries}
    check("atom license has a description",
          by_name["license"].description.startswith("the licensee holds"))
    check("atom license provenance quote",
          by_name["license"].provenance.quote.startswith("Governatori"))

    print("[violation flips]")
    v = d.check(VIOLATION_DDL)
    check("violation theory: pay obligatory", v.verdict("pay") == "obligatory")
    check("violation theory: hasViolation true", v.has_violation)
    # ...and assuming `pay` removes the violation
    v2 = d.check(VIOLATION_DDL, assume=["pay"])
    check("assuming pay clears the violation", not v2.has_violation)

    print("[errors]")
    try:
        d.check("facts: x\nr: x =>O y\n")  # x, y undescribed
        check("undescribed atoms raise", False)
    except DeonticParseError as e:
        check("undescribed atoms raise DeonticParseError",
              "without a description" in str(e))
    try:
        d.check("r1: a =>\n")  # empty conclusion -> Parse error
        check("malformed rule raises", False)
    except DeonticParseError as e:
        check("malformed rule raises DeonticParseError", "Parse error" in str(e))
    try:
        Deontic(binary="/nonexistent/deontic")
        check("missing binary raises", False)
    except DeonticNotBuilt:
        check("missing binary raises DeonticNotBuilt", True)

    print("[llm dispatch]")
    check("TOOL_SCHEMA names run_deontic", TOOL_SCHEMA["name"] == "run_deontic")
    for cmd, args in [("check", []), ("query", ["use"]),
                      ("abduce", ["P(publish)"]), ("atoms", [])]:
        out = dispatch(EX1.read_text(), cmd, args)
        check(f"dispatch {cmd} returns prose", bool(out) and not out.startswith("error"))
    bad = dispatch("nope", "frobnicate")
    check("dispatch unknown command returns error string", bad.startswith("error"))

    print(f"\nALL {PASSED} CHECKS PASSED")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
