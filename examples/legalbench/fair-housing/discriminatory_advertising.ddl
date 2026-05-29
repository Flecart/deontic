# fair-housing — "Is discriminatory advertising prohibited?"  YES.
facts:

atom MakeDiscriminatoryAdvertisement: holds when the provider makes a discriminatory statement or advertisement regarding a dwelling | quote: shall not make any discriminatory statement or advertisement | uri: examples/legalbench/fair-housing/sources/fha.md#L4

discriminatory_advertising: =>O ~MakeDiscriminatoryAdvertisement

# Test:  deontic query <file> MakeDiscriminatoryAdvertisement   ->  F(...)   (prohibited). YES.
