# privacy_policy — "Must a DPIA be done before high-risk processing?"  YES.
facts: HighRiskProcessing

atom HighRiskProcessing: holds when the company plans processing likely to be high-risk to individuals | quote: before high-risk processing
atom ConductDPIA: holds when the company conducts a data protection impact assessment | quote: shall conduct a data protection impact assessment | uri: examples/legalbench/privacy-policy/sources/policies.md#L13

dpia: HighRiskProcessing =>O ConductDPIA

# Test:  deontic query <file> ConductDPIA   ->  O(...)   (high-risk planned). YES.
