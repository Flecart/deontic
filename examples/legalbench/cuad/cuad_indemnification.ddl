# LegalBench cuad_indemnification (CUAD) — ENTAILMENT
# Clause: indemnify the other party against third-party claims arising from breach.
facts: ThirdPartyClaimFromBreach

atom ThirdPartyClaimFromBreach: holds when a third party brings a claim arising from the party's breach | quote: against third-party claims arising from its breach
atom Indemnify: holds when the party indemnifies the other party for that claim | quote: shall indemnify the other party | uri: examples/legalbench/cuad/sources/clauses.md#L16

indemnification: ThirdPartyClaimFromBreach =>O Indemnify

# Test:  deontic query <file> Indemnify   ->  O(Indemnify)   (given the claim). ENTAILMENT.
