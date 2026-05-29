# privacy_policy — "Must the company notify users of a data breach?"  Answer: YES.
facts: DataBreach

atom DataBreach: holds when the company has become aware of a personal data breach | quote: after becoming aware of a personal data breach
atom NotifyUsers: holds when the company notifies affected users of the breach | quote: shall notify affected users without undue delay | uri: examples/legalbench/privacy-policy/sources/policies.md#L2

breach_notice: DataBreach =>O NotifyUsers

# Test:  deontic query <file> NotifyUsers   ->  O(NotifyUsers)   (given a breach). YES.
