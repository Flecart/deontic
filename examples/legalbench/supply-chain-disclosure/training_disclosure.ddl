# supply_chain_disclosure — "Must a covered retailer disclose its training practices?"  YES.
facts: CoveredRetailer

atom CoveredRetailer: holds when the entity is a retailer/manufacturer covered by the Act | quote: A covered retailer
atom DiscloseTrainingPractices: holds when the retailer discloses whether it trains employees on mitigating supply-chain trafficking risks | quote: shall disclose whether it trains employees on mitigating trafficking risks | uri: examples/legalbench/supply-chain-disclosure/sources/sb657.md#L6

training: CoveredRetailer =>O DiscloseTrainingPractices

# Test:  deontic query <file> DiscloseTrainingPractices   ->  O(...)   (covered). YES.
