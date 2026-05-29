# consumer_contracts_qa — "Must the consumer arbitrate disputes?"
# Clause: the consumer must submit any dispute to binding arbitration.  Answer: YES.
facts:

atom Arbitrate: holds when the consumer submits a dispute to binding arbitration | quote: The consumer must submit any dispute to binding arbitration | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L6

arbitration: =>O Arbitrate

# Test:  deontic query <file> Arbitrate   ->  O(Arbitrate)   (mandatory). Answer: YES.
