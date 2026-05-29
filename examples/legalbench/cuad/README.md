# LegalBench cuad — deontic clause types as DDL

Representative formalizations of the **deontic** [CUAD](https://www.atticusprojectai.org/cuad)
clause categories used by LegalBench `cuad_*` tasks. Same approach as
[`../contract-nli/`](../contract-nli/): one `.ddl` per clause type, mandatory
atom descriptions + provenance into [`sources/clauses.md`](sources/clauses.md),
and a footer test. (`B=./.lake/build/bin/deontic`, run from project root.)

| Task (file) | Pattern | Test | Result |
|-------------|---------|------|--------|
| cuad_non-compete | prohibition | `$B query … Compete` | `F(Compete)` |
| cuad_no-solicit-of-employees | prohibition | `$B query … SolicitEmployees` | `F(…)` |
| cuad_covenant-not-to-sue | prohibition | `$B query … Sue` | `F(Sue)` |
| cuad_audit-rights | obligation | `$B query … PermitAudit` | `O(PermitAudit)` |
| cuad_insurance | obligation | `$B query … MaintainInsurance` | `O(…)` |
| cuad_anti-assignment | permission carve-out | `$B abduce … 'P(Assign)' --all` | `{ PriorWrittenConsent }` |
| cuad_termination-for-convenience | permission carve-out | `$B abduce … 'P(Terminate)' --all` | `{ NoticeGiven }` |

These cover CUAD's clause types that express a duty, prohibition, or
conditional permission. Purely descriptive CUAD categories (governing law,
liability cap, IP-ownership, …) aren't deontic and are out of scope for this
reasoner. See [`../COMPARISON.md`](../COMPARISON.md) for the with/without-reasoner
baseline protocol.
