# fcra — "May a CRA furnish a report for a permissible purpose?"  YES (gated).
facts:

atom FurnishConsumerReport: holds when the consumer reporting agency furnishes a consumer report
atom PermissiblePurpose: holds when the request is for a permissible purpose under the Act (credit, employment with consent, etc.) | quote: may furnish a consumer report only for a permissible purpose | uri: examples/legalbench/fcra/sources/fcra.md#L2

no_furnish:    =>O ~FurnishConsumerReport
permissible:   PermissiblePurpose ~>O FurnishConsumerReport
superiority: permissible > no_furnish

# Test:  deontic abduce <file> 'P(FurnishConsumerReport)' --all   ->  { PermissiblePurpose }
#   A report may be furnished only for a permissible purpose. YES (gated).
