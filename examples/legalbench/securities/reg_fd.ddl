# securities — "Must a selective disclosure be publicly disclosed (Reg FD)?"  YES.
facts: SelectiveDisclosure

atom SelectiveDisclosure: holds when the issuer has selectively disclosed material nonpublic information | quote: Upon a selective disclosure of material nonpublic information
atom PublicDisclosure: holds when the issuer makes prompt public disclosure of that information | quote: shall make prompt public disclosure | uri: examples/legalbench/securities/sources/securities.md#L4

reg_fd: SelectiveDisclosure =>O PublicDisclosure

# Test:  deontic query <file> PublicDisclosure   ->  O(...)   (after selective disclosure). YES.
