"""Proposition 1 (Governatori 2018, p.21): coherence and consistency of DDL,
plus the deontic equivalences (eq. 3) and operator interactions (eq. 26-28).

We check the invariants hold structurally across several theories, and assert
the specific entailments the paper ascribes to the operators.
"""

import pytest

from ddl import Literal, lit, parse
from ddl.engine import extension

PERM = ("P", "Ps", "Pw")
ALL = ("C", "O", "P", "Ps", "Pw")


def _atoms_as_literals(theory):
    out = []
    for atom in theory.herbrand_atoms():
        out.append(Literal(atom, False))
        out.append(Literal(atom, True))
    return out


def assert_proposition1(theory):
    """Check the Proposition 1 invariants over the whole extension."""
    e = extension(theory)
    for q in _atoms_as_literals(theory):
        nq = q.complement
        # (1) coherence: never both +dX and -dX
        for mod in ALL:
            assert not (e.has("+", mod, q) and e.has("-", mod, q)), (mod, q)
        # (3) for O and Ps, q and ~q cannot both be positively concluded
        for mod in ("O", "Ps"):
            assert not (e.has("+", mod, q) and e.has("+", mod, nq)), (mod, q)
        # (4) for O and Ps, +dX q implies -dX ~q
        for mod in ("O", "Ps"):
            if e.has("+", mod, q):
                assert e.has("-", mod, nq), (mod, q)
        # (5) not both +dO q and +dPs ~q
        assert not (e.obligation(q) and e.strong_permitted(nq)), q
        # (6) obligation implies permission (P, Ps, Pw)
        if e.obligation(q):
            for mod in PERM:
                assert e.has("+", mod, q), (mod, q)
        # (7) weak permission implies the contrary obligation is refuted
        if e.weak_permitted(q):
            assert e.has("-", "O", nq), q
    return e


THEORIES = {
    "obligation": "=>O p",
    "prohibition": "=>O -p",
    "conflict_resolved": """
        r1: =>O p
        r2: =>O -p
        r2 < r1
    """,
    "uturn": """
        arr40a: AtTrafficLights    =>O -Uturn
        arr40e: UturnPermittedSign ~>O Uturn
        arr40a < arr40e
        AtTrafficLights. UturnPermittedSign.
    """,
    "complaint": """
        tcpc1: ExpressionDissatisfaction => Complaint
        tcpc2: InformationCall           => -Complaint
        tcpc4: AdviseComplaint           => Complaint
        tcpc1 < tcpc2
        tcpc2 < tcpc4
        ExpressionDissatisfaction. InformationCall.
    """,
    "premium": """
        c31:  highSpend       => premiumCustomer
        c32a: specialOrder    => surcharge
        c32b: premiumCustomer => -surcharge
        c32a < c32b
        specialOrder. highSpend.
    """,
}


@pytest.mark.parametrize("name", list(THEORIES))
def test_proposition1_invariants(name):
    assert_proposition1(parse(THEORIES[name]))


def test_obligation_entails_permissions():
    e = extension(parse("=>O p"))
    assert e.obligation(lit("p"))
    assert e.strong_permitted(lit("p"))
    assert e.weak_permitted(lit("p"))
    assert e.permitted(lit("p"))
    assert e.has("-", "O", lit("p", True))  # -dO ~p (no contrary obligation)


def test_prohibition_is_obligation_of_complement():
    # eq.3: F p == O ~p. The parser turns `F p` in a body into O ~p.
    e = extension(parse("=>O -p"))
    assert e.forbidden(lit("p"))  # F p
    assert e.obligation(lit("p", True))  # O ~p, the same conclusion
    assert e.has("-", "O", lit("p"))  # p is not obligatory


def test_weak_but_not_strong_permission_when_unregulated():
    # `drive` is mentioned but no norm forbids it: weakly permitted (nothing to
    # the contrary) but not strongly permitted (no explicit derogating norm).
    # (Out-of-Herbrand-base literals are the query layer's concern, in M4.)
    e = extension(parse("r1: =>O wearSeatbelt\ndrive."))
    assert e.weak_permitted(lit("drive"))  # -dO ~drive holds vacuously
    assert not e.strong_permitted(lit("drive"))
    assert e.permitted(lit("drive"))  # generic permission via weak
