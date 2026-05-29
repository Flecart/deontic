# LegalBench cuad_revenue-sharing (CUAD) — ENTAILMENT
# Clause: pay the other party a share of revenue earned from the licensed product.
facts: RevenueEarned

atom RevenueEarned: holds when the party has earned revenue from the licensed product | quote: revenue earned from the licensed product
atom ShareRevenue: holds when the party pays the other party the agreed revenue share | quote: shall pay the other party a share of revenue earned from the licensed product | uri: examples/legalbench/cuad/sources/clauses.md#L23

revenue_sharing: RevenueEarned =>O ShareRevenue

# Test:  deontic query <file> ShareRevenue   ->  O(...)   (revenue earned). ENTAILMENT.
