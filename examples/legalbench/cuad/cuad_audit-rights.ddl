# LegalBench cuad_audit-rights (CUAD) — ENTAILMENT
# Clause: the party shall permit the other party to audit its records.
facts:

atom PermitAudit: holds when the party permits the other party to audit its records relating to the Agreement | quote: shall permit the other party to audit its records relating to the Agreement | uri: examples/legalbench/cuad/sources/clauses.md#L6

audit_rights: =>O PermitAudit

# Test:  deontic query <file> PermitAudit   ->  O(PermitAudit)   (audit duty ENTAILED)
