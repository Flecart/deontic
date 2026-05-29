# Clause: trade-secret non-disclosure, carve-out only by prior written permission
# ---------------------------------------------------------------------------
# "[Recipient] agrees that, in consideration for being shown or told about
#  certain trade secrets or property belonging to Navidec, Incorporated,
#  [Recipient] shall not disclose or cause to be disclosed, disseminated or
#  distributed any information concerning said trade secret or property to any
#  person, entity, business or other individual or company without the prior
#  written permission of Navidec, Incorporated."
#
# Facts are solved for by reverse search (abduce); no scenario is fixed here.
facts:

# Atom descriptions ground meaning for a fact-finder; after `|` is provenance
# (quote snapshot + uri into the in-repo markdown source with a line selector).
# (This clause names NO employee exception — recipient role is irrelevant, so
# there is deliberately no EmployeeRecipient atom.)
atom Disclose: disclose, disseminate or distribute any information concerning the trade secret or property to any person, entity or business | quote: shall not disclose or cause to be disclosed, disseminated or distributed any information concerning said trade secret or property | uri: examples/clauses/sources/navidec_nda.md#L5-L7
atom PriorWrittenPermission: Navidec, Incorporated has given prior written permission for the disclosure | quote: without the prior written permission of Navidec, Incorporated | uri: examples/clauses/sources/navidec_nda.md#L7-L8

# Recipient shall not disclose the trade secret / property to anyone.
no_disclosure:  =>O  ~Disclose

# The sole carve-out: disclosure with Navidec's prior written permission.
with_permission:  PriorWrittenPermission  ~>O  Disclose

# The specific permission defeats the general prohibition.
superiority: with_permission > no_disclosure

# ---------------------------------------------------------------------------
# Reverse-search questions (abduce):
#
#   deontic abduce examples/clauses/trade_secret_nondisclosure.ddl 'P(Disclose)' --all
#     → POSSIBLE only with: { PriorWrittenPermission }
#       (EmployeeRecipient does not appear — being an employee grants nothing.)
#
#   deontic abduce examples/clauses/trade_secret_nondisclosure.ddl 'P(Disclose)' \
#       --assume EmployeeRecipient,-PriorWrittenPermission
#     → NOT POSSIBLE: unlike disclosure_awareness.ddl, this clause has no
#       employee carve-out, so an employee may receive the trade secret only
#       with Navidec's prior written permission.
# ---------------------------------------------------------------------------
