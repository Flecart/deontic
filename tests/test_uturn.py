"""Example 5 (Governatori 2018): Section 40 of the Australian Road Rules.

"A driver must not make a U-turn at an intersection with traffic lights unless
there is a U-turn permitted sign." Models a prohibition (obligation of the
complement) plus a permissive defeater giving strong permission, which derogates
the prohibition (sect. 3.2).

    arr40a: AtTrafficLights    =>O -Uturn      # F Uturn (prohibition)
    arr40e: UturnPermittedSign ~>O Uturn       # defeater -> strong permission
    arr40a < arr40e                            # the sign derogates the prohibition
"""

from ddl import lit, parse
from ddl.engine import extension

THEORY = """
    arr40a: AtTrafficLights    =>O -Uturn
    arr40e: UturnPermittedSign ~>O Uturn
    arr40a < arr40e
"""

UTURN = lit("Uturn")


def test_uturn_forbidden_at_traffic_lights():
    e = extension(parse(THEORY + "\nAtTrafficLights."))
    assert e.forbidden(UTURN)  # +dO ~Uturn
    assert not e.has("-", "O", UTURN.complement)  # prohibition not refuted
    assert not e.strong_permitted(UTURN)


def test_permitted_sign_derogates_prohibition():
    e = extension(parse(THEORY + "\nAtTrafficLights. UturnPermittedSign."))
    # The prohibition is refuted (-dO ~Uturn) -> the sign defeats arr40a.
    assert not e.forbidden(UTURN)
    assert e.has("-", "O", UTURN.complement)
    # Strong permission to U-turn, and hence generic permission.
    assert e.strong_permitted(UTURN)
    assert e.permitted(UTURN)
    # The defeater cannot make U-turning obligatory.
    assert not e.obligation(UTURN)
