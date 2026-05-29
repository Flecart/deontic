# privacy_policy — "May the company send marketing only with consent?"  YES (gated).
facts:

atom SendMarketing: holds when the company sends marketing communications to the user
atom MarketingConsent: holds when the user has consented to marketing communications | quote: may send marketing communications only with the user's consent | uri: examples/legalbench/privacy-policy/sources/policies.md#L8

no_marketing:   =>O ~SendMarketing
marketing_ok:   MarketingConsent ~>O SendMarketing
superiority: marketing_ok > no_marketing

# Test:  deontic abduce <file> 'P(SendMarketing)' --all   ->  { MarketingConsent }
#   Marketing is permitted only with consent. YES (gated).
