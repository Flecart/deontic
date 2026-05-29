# LegalBench cuad_exclusivity (CUAD) — ENTAILMENT
# Clause: during the term, deal exclusively with the other party; not with competitors.
facts:

atom DealWithCompetitors: holds when the party deals with competitors of the other party during the term | quote: shall not deal with competitors | uri: examples/legalbench/cuad/sources/clauses.md#L10

exclusivity: =>O ~DealWithCompetitors

# Test:  deontic query <file> DealWithCompetitors   ->  F(DealWithCompetitors)   (ENTAILMENT)
