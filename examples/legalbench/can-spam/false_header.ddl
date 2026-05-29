# can-spam — "Is false header information prohibited?"  YES.
facts:

atom UseFalseHeaderInfo: holds when the sender uses false or misleading header information | quote: shall not use false or misleading header information in a commercial email | uri: examples/legalbench/can-spam/sources/canspam.md#L2

false_header: =>O ~UseFalseHeaderInfo

# Test:  deontic query <file> UseFalseHeaderInfo   ->  F(...)   (prohibited). YES.
