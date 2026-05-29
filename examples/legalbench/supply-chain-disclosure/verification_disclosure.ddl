# supply_chain_disclosure — "Must a covered retailer disclose its verification efforts?"  YES.
facts: CoveredRetailer

atom CoveredRetailer: holds when the entity is a retailer/manufacturer covered by the Act | quote: A covered retailer
atom DiscloseVerificationEfforts: holds when the retailer discloses the extent to which it verifies supply chains for trafficking risks | quote: shall disclose the extent to which it verifies product supply chains | uri: examples/legalbench/supply-chain-disclosure/sources/sb657.md#L2

verification: CoveredRetailer =>O DiscloseVerificationEfforts

# Test:  deontic query <file> DiscloseVerificationEfforts   ->  O(...)   (covered). YES.
