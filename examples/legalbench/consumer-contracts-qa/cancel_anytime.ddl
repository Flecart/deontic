# consumer_contracts_qa — "Can the consumer cancel the subscription at any time?"
# Clause grants an unconditional right to cancel.  Answer: YES (permitted).
facts:

atom Cancel: holds when the consumer cancels the subscription | quote: The consumer may cancel the subscription at any time without penalty | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L3

cancel_right: ~>O Cancel

# Test:  deontic query <file> Cancel   ->  Ps(Cancel) / P(Cancel)
#   Cancellation is permitted -> the answer to the question is YES.
