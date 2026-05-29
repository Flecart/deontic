# LegalBench contract_nli_survival_of_obligations  (ContractNLI NDA-19)
# Hypothesis: Some obligations of Agreement may survive termination of Agreement.
# Encoding label: ENTAILMENT
facts:

atom ObligationsSurviveTermination: holds when confidentiality (and related) obligations continue to bind after the Agreement terminates | quote: Some obligations of Agreement may survive termination of Agreement | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L16

survival: => ObligationsSurviveTermination

# Test:  deontic query <file> ObligationsSurviveTermination  ->  fact(ObligationsSurviveTermination)
#   The survival clause is asserted constitutively -> the hypothesis is ENTAILED.
