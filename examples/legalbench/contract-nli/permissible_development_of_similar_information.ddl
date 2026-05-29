# LegalBench contract_nli_permissible_development_of_similar_information  (NDA-17)
# Hypothesis: Receiving Party may independently develop information similar to
# Confidential Information.   Encoding label: ENTAILMENT (carve-out)
facts:

atom UseSimilarInformation: holds when the Receiving Party uses information similar to the Confidential Information
atom IndependentlyDeveloped: holds when that similar information was developed independently, without use of the Confidential Information | quote: may independently develop information similar to Confidential Information | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L14

restrict_similar: =>O ~UseSimilarInformation
develop_carveout: IndependentlyDeveloped ~>O UseSimilarInformation
superiority: develop_carveout > restrict_similar

# Test:  deontic abduce <file> 'P(UseSimilarInformation)' --all  ->  { IndependentlyDeveloped }
#   Use of independently-developed similar info is permitted -> ENTAILED.
