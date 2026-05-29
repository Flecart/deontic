# fcra — "Must a CRA reinvestigate disputed information?"  YES.
facts: ConsumerDispute

atom ConsumerDispute: holds when a consumer has disputed the accuracy of information in their file | quote: Upon a consumer's dispute
atom Reinvestigate: holds when the agency reinvestigates the disputed information | quote: shall reinvestigate the disputed information | uri: examples/legalbench/fcra/sources/fcra.md#L4

reinvestigation: ConsumerDispute =>O Reinvestigate

# Test:  deontic query <file> Reinvestigate   ->  O(...)   (on dispute). YES.
