# can-spam — "Must a sender provide an opt-out mechanism?"  YES.
facts:

atom ProvideOptOutMechanism: holds when the sender provides a clear and functioning opt-out mechanism | quote: shall provide a clear and functioning opt-out mechanism | uri: examples/legalbench/can-spam/sources/canspam.md#L4

opt_out: =>O ProvideOptOutMechanism

# Test:  deontic query <file> ProvideOptOutMechanism   ->  O(...)   (required). YES.
