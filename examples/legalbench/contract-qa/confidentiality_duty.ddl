# contract_qa — "Is the employee barred from disclosing trade secrets?"  YES.
facts:

atom DiscloseEmployerSecrets: holds when the employee discloses the employer's trade secrets | quote: shall not disclose the employer's trade secrets | uri: examples/legalbench/contract-qa/sources/questions.md#L5

confidentiality_duty: =>O ~DiscloseEmployerSecrets

# Test:  deontic query <file> DiscloseEmployerSecrets   ->  F(...)   (prohibited). YES.
