# LegalBench contract_nli_confidentiality_of_agreement  (ContractNLI NDA-10)
# Hypothesis: Receiving Party shall not disclose the fact that Agreement was
# agreed or negotiated.   Encoding label: ENTAILMENT
facts:

atom DiscloseAgreementExistence: holds when the Receiving Party discloses the fact that the Agreement was agreed or negotiated | quote: shall not disclose the fact that Agreement was agreed or negotiated | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L9

confidentiality_of_agreement: =>O ~DiscloseAgreementExistence

# Test:  deontic query <file> DiscloseAgreementExistence   ->  F(DiscloseAgreementExistence)
#   The prohibition is derived, so the hypothesis is ENTAILED.
