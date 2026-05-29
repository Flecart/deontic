# LegalBench cuad_non-compete (CUAD) — ENTAILMENT
# Clause: during the term, the party shall not engage in competing business.
facts:

atom Compete: holds when the party engages in a business that competes with the other party | quote: shall not engage in any business that competes with the other party | uri: examples/legalbench/cuad/sources/clauses.md#L3

non_compete: =>O ~Compete

# Test:  deontic query <file> Compete   ->  F(Compete)   (non-compete duty ENTAILED)
