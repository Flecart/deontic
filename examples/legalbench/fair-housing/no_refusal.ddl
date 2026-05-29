# fair-housing — "Is refusing to rent on a protected basis prohibited?"  YES.
facts:

atom RefuseOnProtectedBasis: holds when the provider refuses to rent or sell a dwelling on a protected basis (race, religion, sex, familial status, disability, etc.) | quote: shall not refuse to rent or sell a dwelling on a protected basis | uri: examples/legalbench/fair-housing/sources/fha.md#L2

no_refusal: =>O ~RefuseOnProtectedBasis

# Test:  deontic query <file> RefuseOnProtectedBasis   ->  F(...)   (prohibited). YES.
