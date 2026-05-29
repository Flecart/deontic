# ecoa — "Must a creditor give an adverse-action notice?"  YES.
facts: AdverseAction

atom AdverseAction: holds when the creditor denies or revokes credit (an adverse action) | quote: when it denies or revokes credit
atom ProvideAdverseActionNotice: holds when the creditor provides a written notice of adverse action | quote: shall provide written notice of adverse action | uri: examples/legalbench/ecoa/sources/ecoa.md#L3

adverse_action: AdverseAction =>O ProvideAdverseActionNotice

# Test:  deontic query <file> ProvideAdverseActionNotice   ->  O(...)   (on adverse action). YES.
