# LegalBench maud — "May a party terminate on a material adverse effect?"  YES (gated).
facts:

atom TerminateForMAE: holds when a party terminates the agreement
atom MaterialAdverseEffect: holds when the other party has suffered a material adverse effect | quote: if the other suffers a material adverse effect | uri: examples/legalbench/maud/sources/dealpoints.md#L7

no_termination: =>O ~TerminateForMAE
mae_out: MaterialAdverseEffect ~>O TerminateForMAE
superiority: mae_out > no_termination

# Test:  deontic abduce <file> 'P(TerminateForMAE)' --all   ->  { MaterialAdverseEffect }
#   Termination is permitted upon an MAE. YES (gated).
