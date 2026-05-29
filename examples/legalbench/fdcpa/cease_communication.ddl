# fdcpa — "Must the collector stop contacting after a written cease request?"  YES.
facts: CeaseRequested

atom CeaseRequested: holds when the consumer has notified the collector in writing to cease communication | quote: If the consumer notifies the collector in writing to cease
atom ContactConsumer: holds when the collector further communicates with the consumer | quote: shall not further communicate with the consumer | uri: examples/legalbench/fdcpa/sources/fdcpa.md#L6

cease_communication: CeaseRequested =>O ~ContactConsumer

# Test:  deontic query <file> ContactConsumer   ->  F(ContactConsumer)   (after a cease request). YES.
