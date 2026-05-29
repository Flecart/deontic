# telemarketing_sales_rule — "Is calling outside 8am-9pm prohibited?"  YES.
facts:

atom CallOutsidePermittedHours: holds when the telemarketer initiates an outbound call before 8 a.m. or after 9 p.m. local time | quote: shall not initiate an outbound call before 8 a.m. or after 9 p.m. local time | uri: examples/legalbench/telemarketing-sales-rule/sources/tsr.md#L4

calling_hours: =>O ~CallOutsidePermittedHours

# Test:  deontic query <file> CallOutsidePermittedHours   ->  F(...)   (prohibited). YES.
