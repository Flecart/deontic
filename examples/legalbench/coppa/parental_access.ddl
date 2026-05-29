# coppa — "Must an operator give a parent access to the child's info?"  YES.
facts: ParentAccessRequest

atom ParentAccessRequest: holds when a parent has requested access to the child's personal information | quote: Upon a parent's request
atom ProvideChildInfoToParent: holds when the operator provides the parent access to the child's information | quote: shall provide the parent access to the child's personal information | uri: examples/legalbench/coppa/sources/coppa.md#L4

parental_access: ParentAccessRequest =>O ProvideChildInfoToParent

# Test:  deontic query <file> ProvideChildInfoToParent   ->  O(...)   (on request). YES.
