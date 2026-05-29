# LegalBench cuad_termination-for-convenience (CUAD) — ENTAILMENT (permitted on notice)
# Clause: a party may terminate for convenience upon prior written notice.
facts:

atom Terminate: holds when the party terminates the Agreement for convenience
atom NoticeGiven: holds when the terminating party has given the required prior written notice | quote: may terminate this Agreement for convenience upon prior written notice | uri: examples/legalbench/cuad/sources/clauses.md#L7

no_terminate: =>O ~Terminate
terminate_on_notice: NoticeGiven ~>O Terminate
superiority: terminate_on_notice > no_terminate

# Test:  deontic abduce <file> 'P(Terminate)' --all   ->  { NoticeGiven }
#   Termination for convenience is permitted once notice is given -> ENTAILED.
