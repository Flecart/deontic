# can-spam — "Must a sender stop emailing after an opt-out?"  YES.
facts: OptedOut

atom OptedOut: holds when the recipient has opted out of commercial email | quote: after they have opted out
atom SendCommercialEmail: holds when the sender sends a commercial email to that recipient | quote: shall not send commercial email to a recipient after they have opted out | uri: examples/legalbench/can-spam/sources/canspam.md#L5

honor_opt_out: OptedOut =>O ~SendCommercialEmail

# Test:  deontic query <file> SendCommercialEmail   ->  F(...)   (after opt-out). YES.
