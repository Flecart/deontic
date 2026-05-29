# LegalBench cuad_post-termination-services (CUAD) — ENTAILMENT
# Clause: upon termination, continue providing transition services for wind-down.
facts: Termination

atom Termination: holds when the Agreement has terminated | quote: Upon termination
atom ProvideTransitionServices: holds when the party continues providing transition/wind-down services after termination | quote: shall continue to provide transition services for the wind-down period | uri: examples/legalbench/cuad/sources/clauses.md#L13

post_termination: Termination =>O ProvideTransitionServices

# Test:  deontic query <file> ProvideTransitionServices   ->  O(...)   (given Termination). ENTAILMENT.
