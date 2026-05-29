# consumer_contracts_qa — "May the company modify the terms at its discretion?"
# Clause grants the company a unilateral right to modify the terms.  Answer: YES.
facts:

atom ModifyTerms: holds when the company modifies the terms of service | quote: The company may modify these terms at any time at its sole discretion | uri: examples/legalbench/consumer-contracts-qa/sources/questions.md#L5

modify_right: ~>O ModifyTerms

# Test:  deontic query <file> ModifyTerms   ->  Ps(ModifyTerms) / P(ModifyTerms)
#   Modification is permitted -> the answer is YES.
