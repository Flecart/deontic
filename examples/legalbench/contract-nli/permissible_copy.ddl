# LegalBench contract_nli_permissible_copy  (ContractNLI NDA-16)
# Hypothesis: Receiving Party may create a copy of some Confidential Information
# in some circumstances.   Encoding label: ENTAILMENT (carve-out)
facts:

atom CopyCI: holds when the Receiving Party makes a copy of Confidential Information
atom AuthorizedNeed: holds when copying is necessary for the permitted purpose of the Agreement | quote: may create a copy of some Confidential Information in some circumstances | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L13

no_copy: =>O ~CopyCI
copy_carveout: AuthorizedNeed ~>O CopyCI
superiority: copy_carveout > no_copy

# Test:  deontic abduce <file> 'P(CopyCI)' --all   ->  { AuthorizedNeed }
#   Copying when needed for the purpose is permitted -> ENTAILED.
