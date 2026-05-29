# hipaa — "Must an accounting of disclosures be provided on request?"  YES.
facts: PatientRequest

atom PatientRequest: holds when the patient has requested an accounting of disclosures | quote: Upon the patient's request
atom ProvideAccounting: holds when the covered entity provides an accounting of disclosures | quote: shall provide an accounting of disclosures | uri: examples/legalbench/hipaa/sources/hipaa.md#L5

accounting: PatientRequest =>O ProvideAccounting

# Test:  deontic query <file> ProvideAccounting   ->  O(...)   (on request). YES.
