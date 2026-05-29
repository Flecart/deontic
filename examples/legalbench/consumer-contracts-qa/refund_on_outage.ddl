# consumer_contracts_qa — "Is the company required to refund on a long outage?"
# Clause: refund owed if the service is unavailable for more than 24 hours.  YES.
facts: ServiceUnavailable24h

atom ServiceUnavailable24h: holds when the service has been unavailable for more than 24 hours | quote: if the service is unavailable for more than 24 hours
atom Refund: holds when the company refunds the consumer | quote: The company shall refund the consumer | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L4

refund: ServiceUnavailable24h =>O Refund

# Test:  deontic query <file> Refund   ->  O(Refund)   (given the outage). Answer: YES.
