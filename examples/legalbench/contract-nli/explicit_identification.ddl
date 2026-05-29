# LegalBench contract_nli_explicit_identification  (ContractNLI NDA-1)
# Hypothesis: All Confidential Information shall be expressly identified by the
# Disclosing Party.   Encoding label: ENTAILMENT
# Modelling: the ONLY way information becomes Confidential Information is by being
# expressly marked/identified, so the reverse search recovers that precondition.
facts:

atom MarkedConfidential: holds when the Disclosing Party has expressly identified/marked the information as confidential | quote: All Confidential Information shall be expressly identified by the Disclosing Party | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L3
atom ConfidentialInformation: holds when the information counts as Confidential Information under the Agreement

identify: MarkedConfidential => ConfidentialInformation

# Test:  deontic abduce <file> 'C(ConfidentialInformation)' --all  ->  { MarkedConfidential }
#   Information is CI only when expressly identified -> the hypothesis is ENTAILED.
