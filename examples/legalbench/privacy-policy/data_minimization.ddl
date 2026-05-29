# privacy_policy — "Is collecting excessive data prohibited?"  YES.
facts:

atom CollectExcessiveData: holds when the company collects personal data beyond what is necessary for the stated purpose | quote: shall not collect personal data beyond what is necessary for the stated purpose | uri: examples/legalbench/privacy-policy/sources/policies.md#L10

data_minimization: =>O ~CollectExcessiveData

# Test:  deontic query <file> CollectExcessiveData   ->  F(CollectExcessiveData)   (prohibited). YES.
