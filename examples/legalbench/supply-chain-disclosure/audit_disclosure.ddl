# supply_chain_disclosure — "Must a covered retailer disclose its audit practices?"  YES.
facts: CoveredRetailer

atom CoveredRetailer: holds when the entity is a retailer/manufacturer covered by the Act | quote: A covered retailer
atom DiscloseAuditPractices: holds when the retailer discloses the extent to which it audits suppliers for compliance | quote: shall disclose the extent to which it audits suppliers for compliance | uri: examples/legalbench/supply-chain-disclosure/sources/sb657.md#L3

audits: CoveredRetailer =>O DiscloseAuditPractices

# Test:  deontic query <file> DiscloseAuditPractices   ->  O(...)   (covered). YES.
