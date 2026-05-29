# telemarketing_sales_rule — "Must the telemarketer transmit caller ID?"  YES.
facts:

atom TransmitCallerID: holds when the telemarketer transmits accurate caller identification information | quote: shall transmit accurate caller identification information | uri: examples/legalbench/telemarketing-sales-rule/sources/tsr.md#L7

caller_id: =>O TransmitCallerID

# Test:  deontic query <file> TransmitCallerID   ->  O(TransmitCallerID)   (required). YES.
