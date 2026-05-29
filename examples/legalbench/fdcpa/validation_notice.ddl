# fdcpa — "Must the collector send a validation notice?"  YES.
facts: InitialCommunication

atom InitialCommunication: holds when the collector has made the initial communication with the consumer | quote: within five days of the initial communication
atom SendValidationNotice: holds when the collector sends the written debt-validation notice | quote: shall send the consumer a written validation notice within five days | uri: examples/legalbench/fdcpa/sources/fdcpa.md#L5

validation_notice: InitialCommunication =>O SendValidationNotice

# Test:  deontic query <file> SendValidationNotice   ->  O(...)   (after initial contact). YES.
