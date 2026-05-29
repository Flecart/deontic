# fdcpa — "Is contacting a consumer at an unusual time prohibited?"  YES.
facts:

atom CommunicateAtUnusualTime: holds when the collector communicates with the consumer before 8am or after 9pm | quote: shall not communicate with a consumer at an unusual or inconvenient time | uri: examples/legalbench/fdcpa/sources/fdcpa.md#L2

unusual_time: =>O ~CommunicateAtUnusualTime

# Test:  deontic query <file> CommunicateAtUnusualTime   ->  F(...)   (prohibited). YES.
