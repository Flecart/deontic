# ada — "Is discrimination on the basis of disability prohibited?"  YES.
facts:

atom DiscriminateOnDisability: holds when the covered entity discriminates against a qualified individual on the basis of disability | quote: shall not discriminate against a qualified individual on the basis of disability | uri: examples/legalbench/ada/sources/ada.md#L2

no_discrimination: =>O ~DiscriminateOnDisability

# Test:  deontic query <file> DiscriminateOnDisability   ->  F(...)   (prohibited). YES.
