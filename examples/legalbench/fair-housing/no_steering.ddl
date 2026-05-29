# fair-housing — "Is steering on a protected basis prohibited?"  YES.
facts:

atom SteerOnProtectedBasis: holds when an agent steers prospective buyers toward or away from neighborhoods on a protected basis | quote: shall not steer prospective buyers on a protected basis | uri: examples/legalbench/fair-housing/sources/fha.md#L6

no_steering: =>O ~SteerOnProtectedBasis

# Test:  deontic query <file> SteerOnProtectedBasis   ->  F(...)   (prohibited). YES.
