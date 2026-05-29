# privacy_policy — "May the user withdraw consent at any time?"  YES.
facts:

atom WithdrawConsent: holds when the user withdraws consent to processing | quote: may withdraw consent to processing at any time | uri: examples/legalbench/privacy-policy/sources/policies.md#L11

withdrawal_right: ~>O WithdrawConsent

# Test:  deontic query <file> WithdrawConsent   ->  Ps(WithdrawConsent) / P(...)
#   Withdrawing consent is permitted -> YES.
