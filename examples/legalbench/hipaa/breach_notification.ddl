# hipaa — "Must individuals be notified of a PHI breach?"  YES.
facts: PHIBreach

atom PHIBreach: holds when there has been a breach of unsecured protected health information | quote: a breach of unsecured PHI
atom NotifyIndividuals: holds when the covered entity notifies the affected individuals | quote: shall notify affected individuals of a breach of unsecured PHI | uri: examples/legalbench/hipaa/sources/hipaa.md#L4

breach_notification: PHIBreach =>O NotifyIndividuals

# Test:  deontic query <file> NotifyIndividuals   ->  O(...)   (given a breach). YES.
