# contract_qa — "Must the employer pay overtime?"  YES.
facts: OvertimeWorked

atom OvertimeWorked: holds when the employee worked more than 40 hours in a week | quote: for hours worked beyond 40 per week
atom PayOvertime: holds when the employer pays overtime for those hours | quote: shall pay overtime for hours worked beyond 40 per week | uri: examples/legalbench/contract-qa/sources/questions.md#L4

overtime: OvertimeWorked =>O PayOvertime

# Test:  deontic query <file> PayOvertime   ->  O(PayOvertime)   (overtime worked). YES.
