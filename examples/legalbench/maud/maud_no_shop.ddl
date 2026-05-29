# LegalBench maud — "Is the target barred from soliciting other offers (no-shop)?"  YES.
facts:

atom SolicitCompetingOffers: holds when the target solicits alternative acquisition proposals | quote: shall not solicit alternative acquisition proposals | uri: examples/legalbench/maud/sources/dealpoints.md#L3

no_shop: =>O ~SolicitCompetingOffers

# Test:  deontic query <file> SolicitCompetingOffers   ->  F(...)   (no-shop). YES.
