# LegalBench cuad_rofr (right of first refusal/offer) (CUAD) — ENTAILMENT (gated)
# Clause: before selling to a third party, first offer the asset to the other party.
facts:

atom SellToThirdParty: holds when the party sells the asset to a third party
atom OfferedToHolderFirst: holds when the asset was first offered to the right-holder (other party) and declined | quote: shall first offer it to the other party | uri: examples/legalbench/cuad/sources/clauses.md#L14

no_thirdparty_sale: =>O ~SellToThirdParty
rofr_satisfied: OfferedToHolderFirst ~>O SellToThirdParty
superiority: rofr_satisfied > no_thirdparty_sale

# Test:  deontic abduce <file> 'P(SellToThirdParty)' --all   ->  { OfferedToHolderFirst }
#   A third-party sale is permitted only after the right-holder was offered first. ENTAILMENT.
