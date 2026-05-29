# LegalBench cuad_source-code-escrow (CUAD) — ENTAILMENT
# Clause: the escrow agent shall release source code upon a release event.
facts: ReleaseEvent

atom ReleaseEvent: holds when a release event (e.g. licensor insolvency) has occurred | quote: upon a release event
atom ReleaseSourceCode: holds when the escrow agent releases the source code to the licensee | quote: shall release the source code to the licensee | uri: examples/legalbench/cuad/sources/clauses.md#L21

source_code_escrow: ReleaseEvent =>O ReleaseSourceCode

# Test:  deontic query <file> ReleaseSourceCode   ->  O(...)   (given a release event). ENTAILMENT.
