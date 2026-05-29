# LegalBench contract_nli_limited_use  (ContractNLI NDA-4)
# Hypothesis: Receiving Party shall not use any Confidential Information for any
# purpose other than the purposes stated in Agreement.   Encoding label: ENTAILMENT
facts:

atom UseForOtherPurpose: holds when the Receiving Party uses Confidential Information for a purpose other than those stated in the Agreement | quote: shall not use any Confidential Information for any purpose other than the purposes stated in Agreement | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L5

limited_use: =>O ~UseForOtherPurpose

# Test:  deontic query <file> UseForOtherPurpose   ->  F(UseForOtherPurpose)
#   The off-purpose-use prohibition is derived, so the hypothesis is ENTAILED.
