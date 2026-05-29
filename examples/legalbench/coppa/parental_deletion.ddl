# coppa — "Must an operator delete a child's info on parental request?"  YES.
facts: ParentDeletionRequest

atom ParentDeletionRequest: holds when a parent has requested deletion of the child's personal information | quote: Upon a parent's request
atom DeleteChildInfo: holds when the operator deletes the child's personal information | quote: shall delete the child's personal information | uri: examples/legalbench/coppa/sources/coppa.md#L5

parental_deletion: ParentDeletionRequest =>O DeleteChildInfo

# Test:  deontic query <file> DeleteChildInfo   ->  O(...)   (on request). YES.
