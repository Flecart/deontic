# ecoa — "Is discouraging a protected applicant prohibited?"  YES.
facts:

atom DiscourageApplicant: holds when the creditor discourages, on a prohibited basis, a prospective applicant from applying | quote: shall not discourage, on a prohibited basis, a prospective applicant from applying for credit | uri: examples/legalbench/ecoa/sources/ecoa.md#L4

no_discouragement: =>O ~DiscourageApplicant

# Test:  deontic query <file> DiscourageApplicant   ->  F(...)   (prohibited). YES.
