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

# Atom descriptions ground the meaning for a fact-finder (human or LLM). After
# `|`: provenance — a quote snapshot and a uri into the in-repo markdown source
# with a GitHub-style line selector (resolve with `deontic atoms --resolve`).
atom Disclose: disclose Confidential Information to any other person (incl. a professional advisor) | quote: prior to the disclosure to any other person ... of any Confidential Information | uri: examples/clauses/sources/nda_confidentiality.md#L3-L6
atom EmployeeRecipient: the other person is an employee of the Receiving Party | quote: The Receiving Party may share some Confidential Information with some of the Receiving Party's employees | uri: examples/clauses/sources/nda_confidentiality.md#L8-L9
atom AwareOfTerms: that person has been made aware of the provisions of this Agreement | quote: made aware of the provisions of this Agreement | uri: examples/clauses/sources/nda_confidentiality.md#L5
atom AwareOfLiability: that person has been made aware that the Disclosee will be liable | quote: the fact that the Disclosee will be liable | uri: examples/clauses/sources/nda_confidentiality.md#L5-L6

# Default: Confidential Information must not be disclosed. The duty is borne by
# the Disclosee / Receiving Party (`@Disclosee`); the Disclosing Party is the
# correlative right-holder, left implicit.
no_disclosure:  =>O@Disclosee  ~Disclose

# Employees may receive Confidential Information, but the procurement clause
# gates it: disclosure is only permitted once the recipient has been made aware
# of (a) the Agreement's provisions and (b) the Disclosee's liability — the
# "prior to the disclosure ... made aware" requirement, modelled as a
# precondition on the employee permission.
employee_disclosure:  EmployeeRecipient, AwareOfTerms, AwareOfLiability  ~>O@Disclosee  Disclose

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
