"""The LLM-facing JSON theory interface and round-tripping with the DSL."""

import pytest

from ddl import lit, parse
from ddl.engine import extension
from ddl.json_io import theory_from_json, theory_to_json
from ddl.parser import ParseError


def test_json_matches_dsl_for_license():
    dsl = parse(open("examples/license.ddl").read()).with_facts(
        parse("license. publish. remove. comment.").facts
    )
    js = theory_from_json(open("examples/license.json").read())
    ed, ej = extension(dsl), extension(js)
    # Same key verdicts from both front-ends.
    for q in (lit("publish", True), lit("comment", True), lit("use", True)):
        assert ed.obligation(q) == ej.obligation(q)
    assert ed.noncompliant() == ej.noncompliant() is True


def test_json_constructs_expected_rules():
    t = theory_from_json(
        {
            "facts": ["highSpend", "specialOrder"],
            "rules": [
                {"id": "c31", "if": ["highSpend"], "then": {"counts_as": "premium"}},
                {"id": "c32a", "if": ["specialOrder"], "then": "surcharge"},
                {"id": "c32b", "if": ["premium"], "then": "-surcharge"},
            ],
            "superiority": [["c32a", "c32b"]],
        }
    )
    e = extension(t)
    assert e.provable(lit("premium"))
    assert e.provable(lit("surcharge", True))  # exemption wins


def test_json_obligation_chain():
    t = theory_from_json(
        {"rules": [{"id": "r", "then": {"obligation": ["-publish", "remove"]}}]}
    )
    assert t.rules[0].mode == "O"
    assert t.rules[0].head == (lit("publish", True), lit("remove"))


def test_roundtrip_dsl_json_dsl():
    src = "r1: a => b\nr2: =>O -x (x) y\na.\nr1 < r2"
    t1 = parse(src)
    t2 = theory_from_json(theory_to_json(t1))
    e1, e2 = extension(t1), extension(t2)
    for q in (lit("b"), lit("x", True), lit("y")):
        assert e1.obligation(q) == e2.obligation(q)
        assert e1.provable(q) == e2.provable(q)


def test_unknown_superiority_rule_errors():
    with pytest.raises(ParseError, match="unknown rule"):
        theory_from_json(
            {"rules": [{"id": "r1", "then": "a"}], "superiority": [["r1", "ghost"]]}
        )


def test_missing_then_errors():
    with pytest.raises(ParseError, match="missing 'then'"):
        theory_from_json({"rules": [{"id": "r1", "if": ["a"]}]})
