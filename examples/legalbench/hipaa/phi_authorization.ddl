# hipaa — "May PHI be disclosed for a non-permitted purpose with authorization?"  YES (gated).
facts:

atom DisclosePHI: holds when the covered entity discloses PHI for a non-permitted purpose
atom PatientAuthorization: holds when the patient has given valid written authorization for the disclosure | quote: only with the patient's authorization | uri: examples/legalbench/hipaa/sources/hipaa.md#L3

no_disclosure:    =>O ~DisclosePHI
authorized_disclosure: PatientAuthorization ~>O DisclosePHI
superiority: authorized_disclosure > no_disclosure

# Test:  deontic abduce <file> 'P(DisclosePHI)' --all   ->  { PatientAuthorization }
#   Disclosure for non-permitted purposes is permitted only with authorization. YES (gated).
