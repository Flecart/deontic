# securities — "Must an insider report ownership changes on Form 4?"  YES.
facts: InsiderTransaction

atom InsiderTransaction: holds when an insider's beneficial ownership has changed | quote: a change in beneficial ownership
atom ReportOnForm4: holds when the insider reports the change on Form 4 within two business days | quote: shall report a change in beneficial ownership on Form 4 within two business days | uri: examples/legalbench/securities/sources/securities.md#L5

section16: InsiderTransaction =>O ReportOnForm4

# Test:  deontic query <file> ReportOnForm4   ->  O(...)   (after a transaction). YES.
