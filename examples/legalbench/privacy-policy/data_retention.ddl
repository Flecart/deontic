# privacy_policy — "Must data be deleted after the retention period?"  YES.
facts: RetentionPeriodExpired

atom RetentionPeriodExpired: holds when the data's retention period has expired | quote: once the retention period expires
atom DeleteAfterRetention: holds when the company deletes the personal data after retention | quote: shall delete personal data once the retention period expires | uri: examples/legalbench/privacy-policy/sources/policies.md#L6

retention: RetentionPeriodExpired =>O DeleteAfterRetention

# Test:  deontic query <file> DeleteAfterRetention   ->  O(...)   (period expired). YES.
