# supply_chain_disclosure — "Must a covered retailer disclose accountability standards?"  YES.
facts: CoveredRetailer

atom CoveredRetailer: holds when the entity is a retailer/manufacturer covered by the Act | quote: A covered retailer
atom DiscloseAccountabilityStandards: holds when the retailer discloses whether it maintains internal accountability standards for non-compliant employees | quote: shall disclose whether it maintains internal accountability standards | uri: examples/legalbench/supply-chain-disclosure/sources/sb657.md#L5

internal_accountability: CoveredRetailer =>O DiscloseAccountabilityStandards

# Test:  deontic query <file> DiscloseAccountabilityStandards   ->  O(...)   (covered). YES.
