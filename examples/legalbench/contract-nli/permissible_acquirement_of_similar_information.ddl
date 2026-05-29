# LegalBench contract_nli_permissible_acquirement_of_similar_information  (NDA-13)
# Hypothesis: Receiving Party may acquire information similar to Confidential
# Information from a third party.   Encoding label: ENTAILMENT (carve-out)
facts:

atom UseSimilarInformation: holds when the Receiving Party uses information similar to the Confidential Information
atom AcquiredFromThirdParty: holds when that similar information was lawfully acquired from a third party | quote: may acquire information similar to Confidential Information from a third party | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L11

restrict_similar: =>O ~UseSimilarInformation
acquired_carveout: AcquiredFromThirdParty ~>O UseSimilarInformation
superiority: acquired_carveout > restrict_similar

# Test:  deontic abduce <file> 'P(UseSimilarInformation)' --all  ->  { AcquiredFromThirdParty }
#   Use of third-party-acquired similar info is permitted -> ENTAILED.
