# Example 3/4 (Governatori 2018): TCPC 2012 definition of a complaint.
# Defeaters and exception-to-exception via superiority.
# Try:  ddl query examples/complaint.ddl "Complaint" \
#         --facts "ExpressionDissatisfaction. InformationCall."
#       (-> not a complaint; add `AdviseComplaint.` -> it is a complaint)

tcpc1: ExpressionDissatisfaction => Complaint
tcpc2: InformationCall           => -Complaint
tcpc3: ProblemCall, FirstCall    ~> Complaint
tcpc4: AdviseComplaint           => Complaint

tcpc1 < tcpc2
tcpc2 < tcpc4
