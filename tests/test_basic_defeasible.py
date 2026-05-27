"""Core basic-defeasible-logic behaviour (Governatori 2018, sect. 3.1).

These exercise the +/-dC proof conditions before any deontic layer: facts,
defeasible rules, conflict, team defeat, defeater-only blocking, and positive
cycles. Conventions verified here: ``r < s`` means s is superior.
"""

from ddl import lit, parse
from ddl.engine import extension


def ext(src: str):
    return extension(parse(src))


def test_fact_is_provable():
    e = ext("a.")
    assert e.provable(lit("a"))
    assert e.refuted(lit("a", True))  # -a is refuted


def test_simple_chain():
    e = ext("""
        a.
        r1: a => b
        r2: b => c
    """)
    assert e.provable(lit("b"))
    assert e.provable(lit("c"))


def test_rule_not_fired_when_premise_absent():
    e = ext("r1: a => b")  # a is not a fact
    assert e.refuted(lit("a"))
    assert e.refuted(lit("b"))


def test_unresolved_conflict_blocks_both():
    # a and -a, no superiority -> ambiguity blocking: neither is provable.
    e = ext("""
        r1: => p
        r2: => -p
    """)
    assert not e.provable(lit("p"))
    assert not e.provable(lit("p", True))
    assert e.refuted(lit("p"))
    assert e.refuted(lit("p", True))


def test_superiority_resolves_conflict():
    e = ext("""
        r1: => p
        r2: => -p
        r2 < r1
    """)
    assert e.provable(lit("p"))
    assert e.refuted(lit("p", True))


def test_team_defeat():
    # Two supporting rules for p, one attacker; one supporter beats the attacker.
    e = ext("""
        a. b. c.
        r1: a => p
        r2: b => p
        r3: c => -p
        r3 < r1
    """)
    assert e.provable(lit("p"))
    assert e.refuted(lit("p", True))


def test_defeater_only_blocks_does_not_prove():
    # A defeater for p can block O¬p style conclusions but cannot itself prove p.
    e = ext("""
        x.
        r1: x ~> p
    """)
    assert not e.provable(lit("p"))  # defeater cannot support
    assert e.refuted(lit("p"))


def test_defeater_blocks_opposing_rule():
    e = ext("""
        x. y.
        r1: x => -p
        r2: y ~> p
        r1 < r2
    """)
    # r2 (defeater) is superior to r1, so r1's conclusion -p is blocked,
    # but r2 cannot prove p either.
    assert not e.provable(lit("p", True))
    assert not e.provable(lit("p"))


def test_positive_cycle_is_refuted():
    # a depends on b and b on a, with no external support: neither is provable.
    e = ext("""
        r1: b => a
        r2: a => b
    """)
    assert e.refuted(lit("a"))
    assert e.refuted(lit("b"))


def test_cycle_attacker_unblocks_conclusion():
    e = ext("""
        r3: => c
        r4: a => -c
        r1: b => a
        r2: a => b
    """)
    # a,b are an unsupported cycle -> -dC, so r4 is discarded and c is provable.
    assert e.refuted(lit("a"))
    assert e.provable(lit("c"))
