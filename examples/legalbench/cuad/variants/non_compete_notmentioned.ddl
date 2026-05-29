# cuad non-compete — NOT-MENTIONED variant.
# Hypothesis: the party is barred from competing.
# This contract addresses only insurance and is silent on competing, so nothing
# forbids it. Label: NOT MENTIONED.
facts:

atom MaintainInsurance: holds when the party maintains the required insurance
atom Compete: holds when the party engages in a competing business | quote: shall not engage in any business that competes with the other party | uri: examples/legalbench/cuad/sources/clauses.md#L3

insurance: =>O MaintainInsurance

# Test:  deontic query <file> Compete   ->  unknown
#   No clause addresses competing -> the non-compete hypothesis is NOT MENTIONED.
