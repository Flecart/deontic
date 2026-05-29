# LegalBench cuad_minimum-commitment (CUAD) — ENTAILMENT
# Clause: the buyer shall purchase at least the minimum quantity each year.
facts:

atom MeetMinimumPurchase: holds when the buyer purchases at least the specified minimum quantity in the period | quote: shall purchase at least the minimum quantity specified each year | uri: examples/legalbench/cuad/sources/clauses.md#L12

minimum_commitment: =>O MeetMinimumPurchase

# Test:  deontic query <file> MeetMinimumPurchase   ->  O(...)   (minimum-commitment ENTAILED)
