# LegalBench hipaa — HIPAA Privacy Rule duties as DDL

Core HIPAA Privacy Rule duties of covered entities over PHI.
(`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| Minimum necessary (`minimum_necessary`) | prohibition | `$B query … UseMoreThanMinimumNecessary` | `F(…)` |
| Authorization for disclosure (`phi_authorization`) | permission carve-out | `$B abduce … 'P(DisclosePHI)' --all` | `{ PatientAuthorization }` |
| Breach notification (`breach_notification`) | cond. obligation | `$B query … NotifyIndividuals` | `O(…)` |
| Accounting of disclosures (`accounting_of_disclosures`) | cond. obligation | `$B query … ProvideAccounting` | `O(…)` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
