# telemarketing_sales_rule — "Must the telemarketer disclose seller identity?"  YES.
facts:

atom DiscloseIdentityAndPurpose: holds when the telemarketer promptly discloses the seller's identity and that the call is a sales call | quote: shall promptly disclose the seller's identity and that the call is a sales call | uri: examples/legalbench/telemarketing-sales-rule/sources/tsr.md#L3

identification: =>O DiscloseIdentityAndPurpose

# Test:  deontic query <file> DiscloseIdentityAndPurpose   ->  O(...)   (required). YES.
