# consumer_contracts_qa — "May the consumer return goods for a refund?"  YES (within window).
facts:

atom ReturnForRefund: holds when the consumer returns goods for a refund
atom WithinReturnWindow: holds when the return is made within 30 days of purchase | quote: may return goods for a refund within 30 days of purchase | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L12

no_return:    =>O ~ReturnForRefund
return_ok:    WithinReturnWindow ~>O ReturnForRefund
superiority: return_ok > no_return

# Test:  deontic abduce <file> 'P(ReturnForRefund)' --all   ->  { WithinReturnWindow }
#   Returns are permitted within the window. YES (conditional).
