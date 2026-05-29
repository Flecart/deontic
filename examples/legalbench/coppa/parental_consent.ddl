# coppa — "May an operator collect a child's info with parental consent?"  YES (gated).
facts:

atom CollectChildInfo: holds when the operator collects personal information from a child under 13
atom VerifiableParentalConsent: holds when the operator has obtained verifiable parental consent | quote: shall obtain verifiable parental consent before collecting personal information from a child under 13 | uri: examples/legalbench/coppa/sources/coppa.md#L2

no_collection:   =>O ~CollectChildInfo
consented_collection: VerifiableParentalConsent ~>O CollectChildInfo
superiority: consented_collection > no_collection

# Test:  deontic abduce <file> 'P(CollectChildInfo)' --all   ->  { VerifiableParentalConsent }
#   Collection is permitted only with verifiable parental consent. YES (gated).
