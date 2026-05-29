# contract_qa — "May the employer terminate at will?"  YES.
facts:

atom TerminateAtWill: holds when the employer terminates the employee at will | quote: may terminate the employee at will | uri: examples/legalbench/contract-qa/sources/questions.md#L3

at_will: ~>O TerminateAtWill

# Test:  deontic query <file> TerminateAtWill   ->  Ps(TerminateAtWill) / P(...)
#   At-will termination is permitted -> YES.
