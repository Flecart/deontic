# LegalBench cuad_most-favored-nation (CUAD) — ENTAILMENT
# Clause: offer terms no less favorable than those offered to any third party.
facts:

atom OfferNoLessFavorableTerms: holds when the party offers the other party terms at least as favorable as any given to a third party | quote: shall offer the other party terms no less favorable than those offered to any third party | uri: examples/legalbench/cuad/sources/clauses.md#L11

mfn: =>O OfferNoLessFavorableTerms

# Test:  deontic query <file> OfferNoLessFavorableTerms   ->  O(...)   (MFN duty ENTAILED)
