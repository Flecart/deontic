# privacy_policy — "Is collecting children's data prohibited?"  YES.
facts:

atom CollectChildData: holds when the company knowingly collects personal data from a child under 13 | quote: shall not knowingly collect personal data from children under 13 | uri: examples/legalbench/privacy-policy/sources/policies.md#L7

childrens_data: =>O ~CollectChildData

# Test:  deontic query <file> CollectChildData   ->  F(CollectChildData)   (prohibited). YES.
