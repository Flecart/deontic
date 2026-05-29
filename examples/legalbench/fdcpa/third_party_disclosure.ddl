# fdcpa — "Is disclosing the debt to third parties prohibited?"  YES.
facts:

atom DiscloseDebtToThirdParty: holds when the collector discloses the debt to a third party other than the consumer or their attorney | quote: shall not disclose the debt to third parties other than the consumer or their attorney | uri: examples/legalbench/fdcpa/sources/fdcpa.md#L7

no_third_party: =>O ~DiscloseDebtToThirdParty

# Test:  deontic query <file> DiscloseDebtToThirdParty   ->  F(...)   (prohibited). YES.
