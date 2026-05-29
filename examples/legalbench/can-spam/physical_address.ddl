# can-spam — "Must a commercial email include a physical address?"  YES.
facts:

atom IncludePhysicalAddress: holds when the email includes a valid physical postal address | quote: shall include a valid physical postal address in the email | uri: examples/legalbench/can-spam/sources/canspam.md#L6

physical_address: =>O IncludePhysicalAddress

# Test:  deontic query <file> IncludePhysicalAddress   ->  O(...)   (required). YES.
