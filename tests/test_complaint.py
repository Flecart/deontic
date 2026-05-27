"""Example 3 / 4 (Governatori 2018): the TCPC 2012 definition of a complaint.

Exercises defeaters and exception-to-exception via the superiority relation.

Note on superiority: the paper's prose superiority line appears garbled, but the
Example 4 *outcomes* it states (tcpc2 defeats tcpc1; adding AdviseComplaint lets
tcpc4 reverse the conclusion) require tcpc1 < tcpc2 and tcpc2 < tcpc4 under the
"s wins" reading. We encode that and check both stated outcomes.

    tcpc1: ExpressionDissatisfaction => Complaint
    tcpc2: InformationCall           => -Complaint
    tcpc3: ProblemCall, FirstCall    ~> Complaint     (defeater)
    tcpc4: AdviseComplaint           => Complaint
"""

from ddl import lit, parse
from ddl.engine import extension

THEORY = """
    tcpc1: ExpressionDissatisfaction => Complaint
    tcpc2: InformationCall           => -Complaint
    tcpc3: ProblemCall, FirstCall    ~> Complaint
    tcpc4: AdviseComplaint           => Complaint
    tcpc1 < tcpc2
    tcpc2 < tcpc4
"""


def test_information_call_is_not_a_complaint():
    # Dissatisfied customer asking for information; AdviseComplaint absent.
    e = extension(parse(THEORY + "\nExpressionDissatisfaction. InformationCall."))
    assert e.provable(lit("Complaint", True))  # +d ~Complaint
    assert e.refuted(lit("Complaint"))  # -d Complaint


def test_advise_complaint_reverses_the_conclusion():
    e = extension(
        parse(
            THEORY
            + "\nExpressionDissatisfaction. InformationCall. AdviseComplaint."
        )
    )
    assert e.provable(lit("Complaint"))  # +d Complaint
    assert e.refuted(lit("Complaint", True))  # -d ~Complaint
