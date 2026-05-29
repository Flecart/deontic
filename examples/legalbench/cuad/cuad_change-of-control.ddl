# LegalBench cuad_change-of-control (CUAD) — ENTAILMENT (gated termination right)
# Clause: on a change of control of a party, the other party may terminate.
facts:

atom TerminateOnChangeOfControl: holds when the other party terminates the Agreement following a change of control
atom ChangeOfControl: holds when a change of control of a party has occurred | quote: Upon a change of control of a party, the other party may terminate the Agreement | uri: examples/legalbench/cuad/sources/clauses.md#L18

no_coc_termination: =>O ~TerminateOnChangeOfControl
coc_termination_ok: ChangeOfControl ~>O TerminateOnChangeOfControl
superiority: coc_termination_ok > no_coc_termination

# Test:  deontic abduce <file> 'P(TerminateOnChangeOfControl)' --all  ->  { ChangeOfControl }
#   Termination is permitted upon a change of control. ENTAILMENT.
