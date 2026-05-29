# telemarketing_sales_rule — "May a prerecorded message be delivered with consent?"  YES (gated).
facts:

atom Robocall: holds when the telemarketer delivers a prerecorded (robocall) message
atom PriorExpressWrittenConsent: holds when the recipient has given prior express written consent to prerecorded messages | quote: without the recipient's prior express written consent | uri: examples/legalbench/telemarketing-sales-rule/sources/tsr.md#L5

no_robocall:    =>O ~Robocall
robocall_ok:    PriorExpressWrittenConsent ~>O Robocall
superiority: robocall_ok > no_robocall

# Test:  deontic abduce <file> 'P(Robocall)' --all   ->  { PriorExpressWrittenConsent }
#   Prerecorded messages are permitted only with prior express written consent. YES (gated).
