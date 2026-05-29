# privacy_policy — "Must the company delete a user's data on request?"  Answer: YES.
facts: DeletionRequest

atom DeletionRequest: holds when the user has requested deletion of their personal data | quote: Upon the user's request
atom DeleteData: holds when the company deletes the user's personal data | quote: shall delete the user's personal data | uri: examples/legalbench/privacy-policy/sources/policies.md#L3

deletion: DeletionRequest =>O DeleteData

# Test:  deontic query <file> DeleteData   ->  O(DeleteData)   (given a request). YES.
