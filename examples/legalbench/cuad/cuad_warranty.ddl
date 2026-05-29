# LegalBench cuad_warranty (CUAD) — ENTAILMENT
# Clause: remedy any defect reported during the warranty period.
facts: DefectReported

atom DefectReported: holds when a defect is reported during the warranty period | quote: any defect reported during the warranty period
atom RemedyDefect: holds when the party remedies the reported defect | quote: shall remedy any defect reported during the warranty period | uri: examples/legalbench/cuad/sources/clauses.md#L24

warranty: DefectReported =>O RemedyDefect

# Test:  deontic query <file> RemedyDefect   ->  O(...)   (defect reported). ENTAILMENT.
