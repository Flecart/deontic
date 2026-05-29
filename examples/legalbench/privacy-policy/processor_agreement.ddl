# privacy_policy — "Must a DPA be in place before engaging a processor?"  YES.
facts: EngagingProcessor

atom EngagingProcessor: holds when the company engages a third-party data processor | quote: before engaging any processor
atom HaveProcessingAgreement: holds when a data processing agreement is in place with that processor | quote: shall enter a data processing agreement before engaging any processor | uri: examples/legalbench/privacy-policy/sources/policies.md#L14

processor_agreement: EngagingProcessor =>O HaveProcessingAgreement

# Test:  deontic query <file> HaveProcessingAgreement   ->  O(...)   (engaging a processor). YES.
