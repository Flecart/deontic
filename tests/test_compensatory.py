"""Compensatory (contrary-to-duty) obligations via the otimes operator, and the
non-compliance tag +d_bottom (Governatori 2018, sect. 2.2, 3.2-3.3, p.20-21).

In ``=>O a (x) b (x) c``: O a is the primary obligation; if it is violated, O b
becomes the in-force (compensatory) obligation; if that too is violated, O c;
once the whole chain is violated the situation is non-compensable (+d_bottom).
A literal counts as violated when its opposite is a fact.
"""

from ddl import lit, parse
from ddl.engine import extension

CHAIN = "r: =>O a (x) b (x) c\n"


def test_primary_obligation_only_when_complied():
    # a is brought about (no violation): only O a; no compensation, no bottom.
    e = extension(parse(CHAIN + "a."))
    assert e.obligation(lit("a"))
    assert not e.obligation(lit("b"))
    assert not e.obligation(lit("c"))
    assert not e.noncompliant()


def test_violation_triggers_compensation():
    # a is violated (-a is a fact): the compensation O b comes into force.
    e = extension(parse(CHAIN + "-a."))
    assert e.obligation(lit("a"))  # the primary obligation is still in force...
    assert e.obligation(lit("b"))  # ...and so is its compensation
    assert not e.obligation(lit("c"))  # b not yet violated
    assert not e.noncompliant()


def test_chained_compensation():
    e = extension(parse(CHAIN + "-a. -b."))
    assert e.obligation(lit("a"))
    assert e.obligation(lit("b"))
    assert e.obligation(lit("c"))  # second compensation in force
    assert not e.noncompliant()  # c is not violated -> still compensable


def test_non_compensable_violation():
    # The whole chain is violated: nothing left to compensate -> +d_bottom.
    e = extension(parse(CHAIN + "-a. -b. -c."))
    assert e.obligation(lit("c"))
    assert e.noncompliant()


def test_otimes_duplication_contraction():
    # a (x) b (x) a normalises to a (x) b (sect. 3.2): the trailing duplicate of
    # a is dropped, so violating a then b is non-compensable.
    e = extension(parse("r: =>O a (x) b (x) a\n-a. -b."))
    assert e.obligation(lit("a"))
    assert e.obligation(lit("b"))
    assert e.noncompliant()
