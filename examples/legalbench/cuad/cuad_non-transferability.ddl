# LegalBench cuad_non-transferability (CUAD) — ENTAILMENT
# Clause: the Agreement is personal and may not be transferred.
facts:

atom Transfer: holds when the party transfers the Agreement to another | quote: may not be transferred | uri: examples/legalbench/cuad/sources/clauses.md#L20

non_transferability: =>O ~Transfer

# Test:  deontic query <file> Transfer   ->  F(Transfer)   (ENTAILMENT)
