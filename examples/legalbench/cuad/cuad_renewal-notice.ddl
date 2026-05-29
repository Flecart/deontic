# LegalBench cuad_renewal-notice (CUAD) — ENTAILMENT
# Clause: give notice of non-renewal at least 60 days before the term ends.
facts: IntendsNonRenewal

atom IntendsNonRenewal: holds when a party intends not to renew the Agreement | quote: notice of non-renewal
atom GiveNonRenewalNotice: holds when the party gives notice of non-renewal at least 60 days before term end | quote: shall give notice of non-renewal at least 60 days before the term ends | uri: examples/legalbench/cuad/sources/clauses.md#L26

renewal_notice: IntendsNonRenewal =>O GiveNonRenewalNotice

# Test:  deontic query <file> GiveNonRenewalNotice   ->  O(...)   (intends non-renewal). ENTAILMENT.
