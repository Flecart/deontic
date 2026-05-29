# LegalBench ecoa — Equal Credit Opportunity Act duties as DDL

Core ECOA creditor duties/prohibitions. (`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| No discrimination (`no_discrimination`) | prohibition | `$B query … DiscriminateOnProhibitedBasis` | `F(…)` |
| No discouragement (`no_discouragement`) | prohibition | `$B query … DiscourageApplicant` | `F(…)` |
| Count protected income (`protected_income`) | prohibition | `$B query … DisregardPublicAssistanceIncome` | `F(…)` |
| Adverse-action notice (`adverse_action_notice`) | cond. obligation | `$B query … ProvideAdverseActionNotice` | `O(…)` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
