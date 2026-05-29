# LegalBench contract_nli_no_licensing  (ContractNLI NDA-11)
# Hypothesis: Agreement shall not grant Receiving Party any right to Confidential
# Information.   Encoding label: ENTAILMENT
# Modelling note: "no right granted" is encoded as a prohibition on the Receiving
# Party acquiring/claiming a right (licence) in the CI — the agreement confers none.
facts:

atom AcquireRightsInCI: holds when the Receiving Party acquires or claims a right (licence) in the Confidential Information | quote: shall not grant Receiving Party any right to Confidential Information | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L10

no_licensing: =>O ~AcquireRightsInCI

# Test:  deontic query <file> AcquireRightsInCI   ->  F(AcquireRightsInCI)
#   The no-rights prohibition is derived, so the hypothesis is ENTAILED.
