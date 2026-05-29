# fair-housing — "Are discriminatory terms prohibited?"  YES.
facts:

atom ImposeDiscriminatoryTerms: holds when the provider imposes different terms or conditions on a protected basis | quote: shall not impose different terms or conditions on a protected basis | uri: examples/legalbench/fair-housing/sources/fha.md#L3

discriminatory_terms: =>O ~ImposeDiscriminatoryTerms

# Test:  deontic query <file> ImposeDiscriminatoryTerms   ->  F(...)   (prohibited). YES.
