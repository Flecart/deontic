# telemarketing_sales_rule — "Is calling a Do-Not-Call number prohibited?"  YES.
facts:

atom CallDNCNumber: holds when the telemarketer calls a number on the National Do Not Call Registry | quote: shall not call any number on the National Do Not Call Registry | uri: examples/legalbench/telemarketing-sales-rule/sources/tsr.md#L2

do_not_call: =>O ~CallDNCNumber

# Test:  deontic query <file> CallDNCNumber   ->  F(CallDNCNumber)   (prohibited). YES.
