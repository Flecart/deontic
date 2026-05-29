# consumer_contracts_qa — "May the consumer opt out of data sale?"  YES.
facts:

atom OptOutOfDataSale: holds when the consumer opts out of the sale of their personal information | quote: may opt out of the sale of their personal information at any time | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L9

opt_out_right: ~>O OptOutOfDataSale

# Test:  deontic query <file> OptOutOfDataSale   ->  Ps(OptOutOfDataSale) / P(...)
#   Opting out is permitted -> Answer: YES.
