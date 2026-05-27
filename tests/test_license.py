"""Example 1 / Section 4 (Governatori 2018): the product-evaluation licence.

This is the paper's headline example -- it defeats possible-worlds approaches.
We reproduce the three narrative scenarios from sect. 1, using the sect. 4
formalisation. The ``r4``/``r4x`` label collision in the paper is read as
``r4`` (publish) and ``r4x`` (use); the superiority is taken verbatim.

    r0:  =>O -use                       # C0 use forbidden by default
    r1:  license ~>O use                # C1 a licence permits use
    r2:  =>O -publish (x) remove        # C2 publishing forbidden, remove compensates
    r2e: approval ~>O publish           # C2e approval permits publishing
    r3:  =>O -comment                   # C3 commenting forbidden
    r3e: P publish ~>O comment          # C3e if publishing is permitted, so is comment
    r4:  commission =>O publish         # C4 commissioned -> must publish
    r4x: commission =>O use             # C4x commissioned -> must use
    r5:  bottom =>O -use                # C5 a non-compensable violation forbids use
"""

from ddl import lit, parse
from ddl.engine import extension

THEORY = """
    r0:  =>O -use
    r1:  license ~>O use
    r2:  =>O -publish (x) remove
    r2e: approval ~>O publish
    r3:  =>O -comment
    r3e: P publish ~>O comment
    r4:  commission =>O publish
    r4x: commission =>O use
    r5:  bottom =>O -use
    r0 < r1
    r0 < r4x
    r1 < r5
    r4x < r2e
    r2 < r2e
    r3 < r3e
"""


def scenario(facts: str):
    return extension(parse(THEORY + "\n" + facts))


def test_a_published_then_removed_in_time():
    # Publishes without approval but removes the material: compensated, so the
    # licence to use still holds.
    e = scenario("license. publish. remove.")
    assert e.forbidden(lit("publish"))  # F publish
    assert e.obligation(lit("remove"))  # O remove (the compensation is in force)
    assert not e.noncompliant()  # the violation was compensated
    assert e.permitted(lit("use"))  # can still legally use the product


def test_b_tweet_without_approval_is_non_compliant():
    # Posts a comment (tweet) without approval to publish: commenting was not
    # permitted, the violation is non-compensable -> can no longer use.
    e = scenario("license. publish. remove. comment.")
    assert e.forbidden(lit("publish"))
    assert not e.permitted(lit("publish"))  # -dP publish
    assert e.forbidden(lit("comment"))  # F comment
    assert e.noncompliant()  # +d_bottom
    assert e.forbidden(lit("use"))  # r5 fires: use is now forbidden
    assert not e.permitted(lit("use"))


def test_c_tweet_after_approval_is_compliant():
    # Obtains approval first: publishing is permitted, so commenting is too,
    # nothing is violated and use continues.
    e = scenario("license. publish. remove. comment. approval.")
    assert e.permitted(lit("publish"))  # approval derogates the prohibition
    assert not e.forbidden(lit("comment"))
    assert e.permitted(lit("comment"))
    assert not e.noncompliant()
    assert e.permitted(lit("use"))
