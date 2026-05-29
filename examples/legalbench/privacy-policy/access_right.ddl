# privacy_policy — "Must the company give the user access to their data?"  Answer: YES.
facts: AccessRequest

atom AccessRequest: holds when the user has requested access to their personal data | quote: Upon the user's request
atom ProvideAccess: holds when the company provides the user access to their personal data | quote: shall provide the user access to their personal data | uri: examples/legalbench/privacy-policy/sources/policies.md#L5

access: AccessRequest =>O ProvideAccess

# Test:  deontic query <file> ProvideAccess   ->  O(ProvideAccess)   (given a request). YES.
