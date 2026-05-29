# telemarketing_sales_rule — "Must total cost be disclosed before payment?"  YES.
facts:

atom DiscloseCostBeforePayment: holds when the telemarketer discloses the total cost and material terms before obtaining payment | quote: shall disclose the total cost and material terms before obtaining payment | uri: examples/legalbench/telemarketing-sales-rule/sources/tsr.md#L8

payment_disclosure: =>O DiscloseCostBeforePayment

# Test:  deontic query <file> DiscloseCostBeforePayment   ->  O(...)   (required). YES.
