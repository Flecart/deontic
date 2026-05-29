# Example 3 & 4: TCPC 2012 complaint definition (§3.1 of Governatori 2018)
# Scenario: customer calls to ask for information about a service
# Facts: ExpressionDissatisfaction (dissatisfied customer), InformationCall (info request)
# AdviseComplaint is NOT a fact
facts: ExpressionDissatisfaction, InformationCall

# tcpc1: if there is expression of dissatisfaction, it is a complaint
tcpc1: ExpressionDissatisfaction => complaint

# tcpc2: if it is an information call, it is NOT a complaint (exception to tcpc1)
tcpc2: InformationCall => ~complaint

# tcpc3: if it is both a problem call and a first call, it MIGHT be a complaint (defeater)
tcpc3: ProblemCall, FirstCall ~> complaint

# tcpc4: if the customer advises they wish to complain, it is a complaint (exception to tcpc2)
tcpc4: AdviseComplaint => complaint

# tcpc2 > tcpc1: information call overrides general expression of dissatisfaction
# tcpc4 > tcpc2: explicit advise to complain overrides information call exception
superiority: tcpc2 > tcpc1, tcpc4 > tcpc2
