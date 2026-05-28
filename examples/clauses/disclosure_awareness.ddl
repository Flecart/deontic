# Clause: third-party disclosure gated on procuring awareness
# ---------------------------------------------------------------------------
# "The Disclosee will procure that, prior to the disclosure to any other person
#  (including any professional advisor) of any Confidential Information, such
#  other person is made aware of the provisions of this Agreement and the fact
#  that the Disclosee will be liable."
# combined with the permission clause:
# "The Receiving Party may share some Confidential Information with some of the
#  Receiving Party's employees."
#
# Facts are solved for by reverse search (abduce); no scenario is fixed here.
facts:

# Atoms
#   Disclose          disclose Confidential Information to another person
#   EmployeeRecipient the other person is an employee of the Receiving Party
#   AwareOfTerms      that person was made aware of the Agreement's provisions
#   AwareOfLiability  that person was made aware the Disclosee will be liable

# Default: Confidential Information must not be disclosed.
no_disclosure:  =>O  ~Disclose

# Employees may receive Confidential Information, but the procurement clause
# gates it: disclosure is only permitted once the recipient has been made aware
# of (a) the Agreement's provisions and (b) the Disclosee's liability — the
# "prior to the disclosure ... made aware" requirement, modelled as a
# precondition on the employee permission.
employee_disclosure:  EmployeeRecipient, AwareOfTerms, AwareOfLiability  ~>O  Disclose

# The specific permission defeats the general prohibition.
superiority: employee_disclosure > no_disclosure

# ---------------------------------------------------------------------------
# Reverse-search questions (abduce):
#
#   deontic abduce examples/clauses/disclosure_awareness.ddl 'P(Disclose)' --all
#     → POSSIBLE, and only when all three hold:
#       { EmployeeRecipient, AwareOfTerms, AwareOfLiability }
#
#   deontic abduce examples/clauses/disclosure_awareness.ddl 'P(Disclose)' \
#       --assume -AwareOfLiability
#     → NOT POSSIBLE: with the liability-awareness withheld, no configuration
#       permits disclosure (the procurement clause bites).
# ---------------------------------------------------------------------------
