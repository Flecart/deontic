# telemarketing_sales_rule — "Must the seller keep telemarketing records?"  YES.
facts:

atom KeepRecords: holds when the seller keeps records of its telemarketing transactions for the required 24 months | quote: shall keep records of its telemarketing transactions for 24 months | uri: examples/legalbench/telemarketing-sales-rule/sources/tsr.md#L9

recordkeeping: =>O KeepRecords

# Test:  deontic query <file> KeepRecords   ->  O(KeepRecords)   (required). YES.
