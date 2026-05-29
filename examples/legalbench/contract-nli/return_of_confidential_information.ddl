# LegalBench contract_nli_return_of_confidential_information  (ContractNLI NDA-15)
# Hypothesis: Receiving Party shall destroy or return some Confidential
# Information upon the termination of Agreement.   Encoding label: ENTAILMENT
facts: Termination

atom Termination: holds when the Agreement is terminated | quote: upon the termination of Agreement
atom ReturnOrDestroyCI: holds when the Receiving Party returns or destroys Confidential Information (the disjunctive duty is modelled as one atom) | quote: shall destroy or return some Confidential Information | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L12

return_ci: Termination =>O ReturnOrDestroyCI

# Test:  deontic query <file> ReturnOrDestroyCI   ->  O(ReturnOrDestroyCI)
#   (given the fact Termination). The return/destroy duty is ENTAILED.
