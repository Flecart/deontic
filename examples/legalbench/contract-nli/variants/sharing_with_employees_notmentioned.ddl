# ContractNLI NDA-5 sharing with employees — NOT-MENTIONED variant.
# Hypothesis: Receiving Party may share some CI with some of its employees.
# This contract only forbids disclosure and says nothing about employees, so the
# permission is unsupported. Label: NOT MENTIONED.
facts:

atom Disclose: holds when the Receiving Party discloses Confidential Information to a person | quote: may share some Confidential Information with some of Receiving Party's employees | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L6

# Blanket confidentiality, no employee carve-out.
no_disclosure: =>O ~Disclose

# Test:  deontic abduce <file> 'P(Disclose)' --all
#     -> "No fact configuration ... makes the goal hold."
#   No clause grants employee sharing -> the hypothesis is NOT MENTIONED
#   (the engine derives no permission; cf. the entailment file which adds a carve-out).
