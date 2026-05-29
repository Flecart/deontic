# LegalBench cuad_liquidated-damages (CUAD) — ENTAILMENT
# Clause: upon a breach, the breaching party shall pay liquidated damages.
facts: Breach

atom Breach: holds when the party has breached the Agreement | quote: Upon a breach
atom PayLiquidatedDamages: holds when the breaching party pays the stipulated liquidated damages | quote: shall pay liquidated damages | uri: examples/legalbench/cuad/sources/clauses.md#L22

liquidated_damages: Breach =>O PayLiquidatedDamages

# Test:  deontic query <file> PayLiquidatedDamages   ->  O(...)   (given a breach). ENTAILMENT.
