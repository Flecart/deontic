# cuad non-compete — CONTRADICTION variant.
# Hypothesis: the party is barred from competing.
# This contract expressly permits the party to engage in other businesses, so the
# hypothesis is CONTRADICTED.
facts: OtherBusinessPermitted

atom Compete: holds when the party engages in a competing business | quote: shall not engage in any business that competes with the other party | uri: examples/legalbench/cuad/sources/clauses.md#L3
atom OtherBusinessPermitted: holds when the agreement expressly permits the party to engage in other (including competing) businesses

permit_compete: OtherBusinessPermitted ~>O Compete

# Test:  deontic query <file> Compete   ->  Ps(Compete) / P(...)
#   Competing is permitted, contradicting the non-compete prohibition the
#   hypothesis asserts. Label: CONTRADICTION.
