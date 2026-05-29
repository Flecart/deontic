# coppa — "Is conditioning participation on excessive info prohibited?"  YES.
facts:

atom ConditionParticipationOnExcessiveInfo: holds when the operator conditions a child's participation on disclosing more information than is reasonably necessary | quote: shall not condition a child's participation in an activity on disclosing more information than is reasonably necessary | uri: examples/legalbench/coppa/sources/coppa.md#L6

no_conditioning: =>O ~ConditionParticipationOnExcessiveInfo

# Test:  deontic query <file> ConditionParticipationOnExcessiveInfo   ->  F(...)   (prohibited). YES.
