# consumer_contracts_qa — "May the company assign the agreement without consent?"  YES.
facts:

atom AssignToSuccessor: holds when the company assigns the agreement to a successor without the consumer's consent | quote: may assign this agreement to a successor without the consumer's consent | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L11

company_assignment: ~>O AssignToSuccessor

# Test:  deontic query <file> AssignToSuccessor   ->  Ps(AssignToSuccessor) / P(...)
#   Assignment to a successor is permitted -> Answer: YES.
