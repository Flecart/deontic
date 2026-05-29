# A single NDA theory answering MULTIPLE contract_nli hypotheses coherently —
# the cross-hypothesis consistency the COMPARISON.md baseline argues for.
# Scenario facts: the RP is compelled by law and the agreement has terminated.
facts: CompelledByLaw, Termination

atom UseForOtherPurpose:    holds when the RP uses CI for a purpose other than those stated | quote: shall not use any Confidential Information for any purpose other than the purposes stated in Agreement | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L5
atom Disclose:              holds when the RP discloses CI to a recipient
atom EmployeeRecipient:     holds when the recipient is an employee of the RP | quote: may share some Confidential Information with some of Receiving Party's employees | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L6
atom CompelledByLaw:        holds when the RP is legally compelled to disclose CI
atom NotifyDisclosingParty: holds when the RP notifies the DP of a compelled disclosure | quote: shall notify Disclosing Party | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L8
atom Termination:           holds when the Agreement has terminated
atom ReturnOrDestroyCI:     holds when the RP returns or destroys CI | quote: shall destroy or return some Confidential Information | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L12
atom ObligationsSurviveTermination: holds when obligations continue after termination | quote: Some obligations of Agreement may survive termination of Agreement | uri: examples/legalbench/contract-nli/sources/hypotheses.md#L16

limited_use:    =>O ~UseForOtherPurpose
no_disclosure:  =>O ~Disclose
share_employee: EmployeeRecipient ~>O Disclose
notice:         CompelledByLaw =>O NotifyDisclosingParty
return_ci:      Termination =>O ReturnOrDestroyCI
survival:       => ObligationsSurviveTermination
superiority: share_employee > no_disclosure

# One theory, many hypotheses (all consistent):
#   query UseForOtherPurpose          -> F   (limited use)            ENTAIL
#   query NotifyDisclosingParty       -> O   (notice, compelled)      ENTAIL
#   query ReturnOrDestroyCI           -> O   (return, terminated)     ENTAIL
#   query ObligationsSurviveTermination -> fact (survival)           ENTAIL
#   abduce 'P(Disclose)' --all        -> { EmployeeRecipient }        ENTAIL (sharing w/ employees)
