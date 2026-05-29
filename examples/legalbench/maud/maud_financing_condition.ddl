# LegalBench maud — "Must the buyer close even without financing?"  YES (no financing condition).
facts:

atom RefuseToCloseForLackOfFinancing: holds when the buyer refuses to close citing failure to obtain financing | quote: shall close even if it fails to obtain financing (no financing condition) | uri: examples/legalbench/maud/sources/dealpoints.md#L6

no_financing_condition: =>O ~RefuseToCloseForLackOfFinancing

# Test:  deontic query <file> RefuseToCloseForLackOfFinancing   ->  F(...)
#   The buyer may not refuse to close for lack of financing -> YES (no financing out).
