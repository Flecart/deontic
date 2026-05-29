# LegalBench cuad_covenant-not-to-sue (CUAD) — ENTAILMENT
# Clause: the party covenants not to sue the other party re the licensed matter.
facts:

atom Sue: holds when the party brings suit against the other party in respect of the licensed matter | quote: covenants not to sue the other party in respect of the licensed matter | uri: examples/legalbench/cuad/sources/clauses.md#L9

covenant_not_to_sue: =>O ~Sue

# Test:  deontic query <file> Sue   ->  F(Sue)   (covenant not to sue ENTAILED)
