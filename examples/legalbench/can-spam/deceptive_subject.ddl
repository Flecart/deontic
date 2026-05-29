# can-spam — "Is a deceptive subject line prohibited?"  YES.
facts:

atom UseDeceptiveSubject: holds when the sender uses a deceptive or misleading subject line | quote: shall not use a deceptive or misleading subject line | uri: examples/legalbench/can-spam/sources/canspam.md#L3

deceptive_subject: =>O ~UseDeceptiveSubject

# Test:  deontic query <file> UseDeceptiveSubject   ->  F(...)   (prohibited). YES.
