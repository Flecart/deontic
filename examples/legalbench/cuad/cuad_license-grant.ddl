# LegalBench cuad_license-grant (CUAD) — ENTAILMENT (permission)
# Clause: the licensor grants the licensee a license to use the software in term.
facts:

atom UseLicensedSoftware: holds when the licensee uses the licensed software | quote: grants the licensee a license to use the licensed software during the term | uri: examples/legalbench/cuad/sources/clauses.md#L17

license_grant: ~>O UseLicensedSoftware

# Test:  deontic query <file> UseLicensedSoftware   ->  Ps(UseLicensedSoftware) / P(...)
#   The grant permits use -> ENTAILMENT (a permission, not a duty).
