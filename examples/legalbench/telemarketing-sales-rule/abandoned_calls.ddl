# telemarketing_sales_rule — "Is abandoning more than 3% of calls prohibited?"  YES.
facts:

atom AbandonExcessCalls: holds when the telemarketer abandons more than three percent of answered calls | quote: shall not abandon more than three percent of answered calls | uri: examples/legalbench/telemarketing-sales-rule/sources/tsr.md#L6

abandoned_calls: =>O ~AbandonExcessCalls

# Test:  deontic query <file> AbandonExcessCalls   ->  F(AbandonExcessCalls)   (prohibited). YES.
