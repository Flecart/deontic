# ecoa — "Is disregarding public-assistance income prohibited?"  YES.
facts:

atom DisregardPublicAssistanceIncome: holds when the creditor disregards income derived from public assistance in evaluating creditworthiness | quote: shall not disregard income derived from public assistance | uri: examples/legalbench/ecoa/sources/ecoa.md#L5

protected_income: =>O ~DisregardPublicAssistanceIncome

# Test:  deontic query <file> DisregardPublicAssistanceIncome   ->  F(...)   (prohibited). YES.
