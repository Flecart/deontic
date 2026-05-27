"""The high-level Reasoner/Verdict facade and query parsing."""

from ddl import Reasoner
from ddl.api import parse_query
from ddl.proof import Conclusion
from ddl.syntax import BOTTOM, lit


def test_parse_query_forms():
    assert parse_query("+dO remove") == Conclusion("+", "O", lit("remove"))
    assert parse_query("-dC publish") == Conclusion("-", "C", lit("publish"))
    assert parse_query("O remove") == Conclusion("+", "O", lit("remove"))
    assert parse_query("F publish") == Conclusion("+", "O", lit("publish", True))
    assert parse_query("Ps use") == Conclusion("+", "Ps", lit("use"))
    assert parse_query("publish") == Conclusion("+", "C", lit("publish"))
    assert parse_query("noncompliant") == Conclusion("+", "⊥", BOTTOM)


def test_friendly_query_against_uturn():
    r = Reasoner.from_ddl(
        "arr40a: AtTrafficLights =>O -Uturn\n"
        "arr40e: UturnPermittedSign ~>O Uturn\n"
        "arr40a < arr40e\n"
        "AtTrafficLights. UturnPermittedSign."
    )
    assert r.holds("Ps Uturn")
    assert not r.holds("F Uturn")
    assert r.query("F Uturn").holds is False


def test_verdict_has_trace():
    r = Reasoner.from_ddl(
        "tcpc1: Diss => Complaint\n"
        "tcpc2: Info => -Complaint\n"
        "tcpc4: Advise => Complaint\n"
        "tcpc1 < tcpc2\n tcpc2 < tcpc4\n"
        "Diss. Info. Advise."
    )
    v = r.query("Complaint")
    assert v.holds
    assert any("tcpc4" in line for line in v.trace)


def test_out_of_base_literal_is_weakly_permitted():
    # `swim` is not mentioned anywhere; nothing forbids it -> weakly permitted,
    # generically permitted, but not obligatory and not strongly permitted.
    r = Reasoner.from_ddl("r: =>O wearSeatbelt\ndrive.")
    assert r.holds("Pw swim")
    assert r.holds("P swim")
    assert not r.holds("O swim")
    assert not r.holds("Ps swim")


def test_what_if_extra_facts_flip_verdict():
    r = Reasoner.from_ddl(open("examples/license.ddl").read())
    base = r.with_facts({lit("license"), lit("publish"), lit("remove")})
    assert not base.query("noncompliant").holds  # compensated
    appealed = r.with_facts(
        {lit("license"), lit("publish"), lit("remove"), lit("comment")}
    )
    assert appealed.query("noncompliant").holds  # uncompensated comment
