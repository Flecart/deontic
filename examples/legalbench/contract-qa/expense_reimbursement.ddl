# contract_qa — "Must the employer reimburse approved expenses?"  YES.
facts: ApprovedExpense

atom ApprovedExpense: holds when the employee has incurred an approved business expense | quote: approved business expenses
atom Reimburse: holds when the employer reimburses that expense | quote: shall reimburse approved business expenses | uri: examples/legalbench/contract-qa/sources/questions.md#L6

reimbursement: ApprovedExpense =>O Reimburse

# Test:  deontic query <file> Reimburse   ->  O(Reimburse)   (approved expense). YES.
