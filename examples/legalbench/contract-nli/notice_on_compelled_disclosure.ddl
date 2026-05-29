# LegalBench contract_nli_notice_on_compelled_disclosure  (ContractNLI NDA-8)
# Hypothesis: Receiving Party shall notify Disclosing Party if required by law,
# regulation or judicial process to disclose Confidential Information.  ENTAILMENT
facts: CompelledByLaw

atom CompelledByLaw: holds when the Receiving Party is required by law, regulation or judicial process to disclose Confidential Information | quote: required by law, regulation or judicial process to disclose
atom NotifyDisclosingParty: holds when the Receiving Party notifies the Disclosing Party of the compelled disclosure | quote: shall notify Disclosing Party | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L8

notice: CompelledByLaw =>O NotifyDisclosingParty

# Test:  deontic query <file> NotifyDisclosingParty   ->  O(NotifyDisclosingParty)
#   (given the fact CompelledByLaw). The notification duty is ENTAILED.
