# maud no-shop — CONTRADICTION variant.
# Hypothesis: the target shall not solicit alternative proposals (no-shop).
# This agreement instead includes a GO-SHOP period permitting solicitation, so the
# hypothesis is CONTRADICTED.
facts: GoShopPeriod

atom SolicitCompetingOffers: holds when the target solicits alternative acquisition proposals | quote: shall not solicit alternative acquisition proposals | uri: examples/legalbench/maud/sources/dealpoints.md#L3
atom GoShopPeriod: holds when the agreement includes a go-shop period expressly permitting solicitation

go_shop: GoShopPeriod ~>O SolicitCompetingOffers

# Test:  deontic query <file> SolicitCompetingOffers   ->  Ps(...) / P(...)
#   Solicitation is permitted, contradicting the no-shop prohibition the
#   hypothesis asserts. Label: CONTRADICTION.
