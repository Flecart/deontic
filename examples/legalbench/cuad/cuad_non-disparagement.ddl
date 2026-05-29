# LegalBench cuad_non-disparagement (CUAD) — ENTAILMENT
# Clause: the party shall not make disparaging statements about the other party.
facts:

atom Disparage: holds when the party makes a disparaging statement about the other party | quote: shall not make any disparaging statements about the other party | uri: examples/legalbench/cuad/sources/clauses.md#L15

non_disparagement: =>O ~Disparage

# Test:  deontic query <file> Disparage   ->  F(Disparage)   (ENTAILMENT)
