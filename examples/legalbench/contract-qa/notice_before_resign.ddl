# contract_qa — "Must the employee give notice before resigning?"  YES.
facts: Resigning

atom Resigning: holds when the employee intends to resign | quote: before resigning
atom GiveTwoWeeksNotice: holds when the employee gives two weeks' notice | quote: shall give two weeks' notice before resigning | uri: examples/legalbench/contract-qa/sources/questions.md#L2

notice_before_resign: Resigning =>O GiveTwoWeeksNotice

# Test:  deontic query <file> GiveTwoWeeksNotice   ->  O(...)   (when resigning). YES.
