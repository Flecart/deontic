# LegalBench contract_nli_sharing_with_employees  (ContractNLI NDA-5)
# Hypothesis: Receiving Party may share some Confidential Information with some of
# Receiving Party's employees.   Encoding label: ENTAILMENT (permitted, gated)
facts:

atom Disclose: holds when the Receiving Party discloses Confidential Information to the recipient
atom EmployeeRecipient: holds when the recipient is an employee of the Receiving Party | quote: may share some Confidential Information with some of Receiving Party's employees | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L6

no_disclosure:  =>O  ~Disclose
share_employee: EmployeeRecipient  ~>O  Disclose
superiority: share_employee > no_disclosure

# Test:  deontic abduce <file> 'P(Disclose)' --all   ->  { EmployeeRecipient }
#   Disclosure to an employee is permitted, so the hypothesis is ENTAILED.
