# consumer_contracts_qa — "May the consumer dispute an erroneous charge?"  YES.
facts:

atom DisputeCharge: holds when the consumer disputes a charge they believe is erroneous | quote: may dispute any charge they believe is erroneous | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L13

dispute_right: ~>O DisputeCharge

# Test:  deontic query <file> DisputeCharge   ->  Ps(DisputeCharge) / P(...)
#   Disputing a charge is permitted -> YES.
