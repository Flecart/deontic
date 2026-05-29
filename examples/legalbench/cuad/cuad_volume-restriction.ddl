# LegalBench cuad_volume-restriction (CUAD) — ENTAILMENT
# Clause: the buyer shall not purchase more than the maximum quantity per period.
facts:

atom ExceedVolumeLimit: holds when the buyer purchases more than the maximum quantity per period | quote: shall not purchase more than the maximum quantity per period | uri: examples/legalbench/cuad/sources/clauses.md#L25

volume_restriction: =>O ~ExceedVolumeLimit

# Test:  deontic query <file> ExceedVolumeLimit   ->  F(ExceedVolumeLimit)   (ENTAILMENT)
