# ContractNLI NDA-4 limited use — CONTRADICTION variant.
# Hypothesis: Receiving Party shall not use CI for any purpose other than stated.
# This contract instead GRANTS broad use, so the hypothesis is CONTRADICTED.
facts: BroadPurposeGranted

atom UseForOtherPurpose: holds when the Receiving Party uses Confidential Information for a purpose other than those stated | quote: shall not use any Confidential Information for any purpose other than the purposes stated in Agreement | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L5
atom BroadPurposeGranted: holds when the Agreement grants the Receiving Party use of CI for any purpose

broad_use: BroadPurposeGranted ~>O UseForOtherPurpose

# Test:  deontic query <file> UseForOtherPurpose   ->  Ps(UseForOtherPurpose) / P(...)
#   Off-purpose use is permitted, which contradicts the prohibition the
#   hypothesis asserts (F(UseForOtherPurpose)). Label: CONTRADICTION.
