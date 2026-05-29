# securities — "Must an insider disgorge short-swing profits?"  YES.
facts: ShortSwingProfit

atom ShortSwingProfit: holds when an insider realized a profit from a purchase and sale within a six-month period | quote: profits from any purchase and sale within a six-month period
atom DisgorgeProfit: holds when the insider disgorges that profit to the issuer | quote: shall disgorge profits from any purchase and sale within a six-month period | uri: examples/legalbench/securities/sources/securities.md#L6

short_swing: ShortSwingProfit =>O DisgorgeProfit

# Test:  deontic query <file> DisgorgeProfit   ->  O(...)   (short-swing profit). YES.
