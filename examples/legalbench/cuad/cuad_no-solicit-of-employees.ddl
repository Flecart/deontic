# LegalBench cuad_no-solicit-of-employees (CUAD) — ENTAILMENT
# Clause: the party shall not solicit for employment the other party's employees.
facts:

atom SolicitEmployees: holds when the party solicits for employment an employee of the other party | quote: shall not solicit for employment any employee of the other party | uri: examples/legalbench/cuad/sources/clauses.md#L4

no_solicit: =>O ~SolicitEmployees

# Test:  deontic query <file> SolicitEmployees   ->  F(SolicitEmployees)   (ENTAILMENT)
