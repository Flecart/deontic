# ecoa — "Is discrimination on a prohibited basis barred?"  YES.
facts:

atom DiscriminateOnProhibitedBasis: holds when the creditor discriminates against an applicant on a prohibited basis (race, religion, sex, age, etc.) | quote: shall not discriminate against an applicant on a prohibited basis | uri: examples/legalbench/ecoa/sources/ecoa.md#L2

no_discrimination: =>O ~DiscriminateOnProhibitedBasis

# Test:  deontic query <file> DiscriminateOnProhibitedBasis   ->  F(...)   (prohibited). YES.
