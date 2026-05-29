# LegalBench cuad_insurance (CUAD) — ENTAILMENT
# Clause: the party shall maintain specified insurance during the term.
facts:

atom MaintainInsurance: holds when the party maintains insurance of the specified types and amounts | quote: shall maintain insurance of the types and amounts specified during the term | uri: examples/legalbench/cuad/sources/clauses.md#L8

insurance: =>O MaintainInsurance

# Test:  deontic query <file> MaintainInsurance   ->  O(MaintainInsurance)   (ENTAILMENT)
