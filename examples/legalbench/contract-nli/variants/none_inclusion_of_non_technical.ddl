# ContractNLI NDA-2 none-inclusion of non-technical information
# Hypothesis: Confidential Information shall only include technical information.
# Encoding label: ENTAILMENT (technical info is CI's sole classification path)
facts:

atom TechnicalInfo: holds when the information is technical in nature | quote: Confidential Information shall only include technical information | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L17
atom ConfidentialInformation: holds when the information counts as Confidential Information under the Agreement

only_technical: TechnicalInfo => ConfidentialInformation

# Test:  deontic abduce <file> 'C(ConfidentialInformation)' --all  ->  { TechnicalInfo }
#   The only way to be CI is to be technical -> "only technical" is ENTAILED.
