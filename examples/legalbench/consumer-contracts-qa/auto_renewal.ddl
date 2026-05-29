# consumer_contracts_qa — "Will the subscription auto-renew?"  YES (unless cancelled).
facts:

atom AutoRenews: holds when the subscription renews automatically for a successive term | quote: shall automatically renew for successive terms | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L8
atom CancelBeforeRenewal: holds when the consumer cancels before the renewal date

auto_renew:  => AutoRenews
cancel_stops: CancelBeforeRenewal ~> ~AutoRenews
superiority: cancel_stops > auto_renew

# Test:  deontic query <file> AutoRenews   ->  fact(AutoRenews)   (no cancellation). Answer: YES.
#   (Cancelling before renewal defeats it; see abduce 'C(~AutoRenews)' style checks.)
