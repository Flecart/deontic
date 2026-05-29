# LegalBench cuad_anti-assignment (CUAD) — ENTAILMENT (assignment gated on consent)
# Clause: neither party may assign without the other party's prior written consent.
facts:

atom Assign: holds when the party assigns the Agreement to a third party
atom PriorWrittenConsent: holds when the other party has given prior written consent to the assignment | quote: may assign this Agreement without the prior written consent of the other party | uri: examples/legalbench/cuad/sources/clauses.md#L5

no_assign: =>O ~Assign
assign_with_consent: PriorWrittenConsent ~>O Assign
superiority: assign_with_consent > no_assign

# Test:  deontic abduce <file> 'P(Assign)' --all   ->  { PriorWrittenConsent }
#   Assignment is permitted only with consent -> the anti-assignment clause is ENTAILED.
