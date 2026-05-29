# privacy_policy — "May the company share data with third-party providers?"  YES (gated).
facts:

atom ShareData: holds when the company shares personal data with a third party
atom ServiceProviderPurpose: holds when the recipient is a third-party service provider engaged to operate the service | quote: may share personal data with third-party service providers to operate the service | uri: examples/legalbench/privacy-policy/sources/policies.md#L4

no_sharing:     =>O ~ShareData
provider_share: ServiceProviderPurpose ~>O ShareData
superiority: provider_share > no_sharing

# Test:  deontic abduce <file> 'P(ShareData)' --all   ->  { ServiceProviderPurpose }
#   Sharing is permitted for service-provider purposes -> YES.
