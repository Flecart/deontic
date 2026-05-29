# privacy_policy — "May data be transferred abroad with safeguards?"  YES (gated).
facts:

atom TransferAbroad: holds when the company transfers personal data to another country
atom AppropriateSafeguards: holds when appropriate transfer safeguards (e.g. SCCs) are in place | quote: may transfer personal data abroad only with appropriate safeguards | uri: examples/legalbench/privacy-policy/sources/policies.md#L12

no_transfer_abroad: =>O ~TransferAbroad
transfer_ok:        AppropriateSafeguards ~>O TransferAbroad
superiority: transfer_ok > no_transfer_abroad

# Test:  deontic abduce <file> 'P(TransferAbroad)' --all   ->  { AppropriateSafeguards }
#   Cross-border transfer is permitted only with safeguards. YES (gated).
