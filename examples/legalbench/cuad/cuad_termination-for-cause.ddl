# LegalBench cuad_termination-for-cause (CUAD) — ENTAILMENT (breach-gated right)
# Clause: a party may terminate for cause upon the other party's material breach.
facts:

atom TerminateForCause: holds when the party terminates the Agreement for cause
atom MaterialBreach: holds when the other party has materially breached the Agreement | quote: may terminate the Agreement for cause upon the other party's material breach | uri: examples/legalbench/cuad/sources/clauses.md#L19

no_termination:  =>O ~TerminateForCause
cause_termination: MaterialBreach ~>O TerminateForCause
superiority: cause_termination > no_termination

# Test:  deontic abduce <file> 'P(TerminateForCause)' --all  ->  { MaterialBreach }
#   Termination for cause is permitted upon material breach. ENTAILMENT.
