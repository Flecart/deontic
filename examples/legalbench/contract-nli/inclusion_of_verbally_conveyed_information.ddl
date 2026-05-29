# LegalBench contract_nli_inclusion_of_verbally_conveyed_information  (NDA-3)
# Hypothesis: Confidential Information may include verbally conveyed information.
# Encoding label: ENTAILMENT
facts:

atom VerballyConveyed: holds when information was conveyed orally/verbally | quote: Confidential Information may include verbally conveyed information | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L4
atom ConfidentialInformation: holds when the information counts as Confidential Information under the Agreement

verbal_inclusion: VerballyConveyed => ConfidentialInformation

# Test:  deontic abduce <file> 'C(ConfidentialInformation)' --all  ->  { VerballyConveyed }
#   Verbally-conveyed information can be CI -> the hypothesis is ENTAILED.
