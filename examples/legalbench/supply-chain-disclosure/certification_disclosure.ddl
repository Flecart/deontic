# supply_chain_disclosure — "Must a covered retailer disclose its certification requirement?"  YES.
facts: CoveredRetailer

atom CoveredRetailer: holds when the entity is a retailer/manufacturer covered by the Act | quote: A covered retailer
atom DiscloseCertificationRequirement: holds when the retailer discloses whether it requires suppliers to certify anti-trafficking compliance | quote: shall disclose whether it requires suppliers to certify | uri: examples/legalbench/supply-chain-disclosure/sources/sb657.md#L4

certification: CoveredRetailer =>O DiscloseCertificationRequirement

# Test:  deontic query <file> DiscloseCertificationRequirement   ->  O(...)   (covered). YES.
