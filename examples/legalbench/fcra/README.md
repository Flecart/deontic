# LegalBench fcra — Fair Credit Reporting Act duties as DDL

Core FCRA duties of consumer reporting agencies and users.
(`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| Permissible purpose (`permissible_purpose`) | permission carve-out | `$B abduce … 'P(FurnishConsumerReport)' --all` | `{ PermissiblePurpose }` |
| Accuracy procedures (`accuracy_procedures`) | obligation | `$B query … FollowAccuracyProcedures` | `O(…)` |
| Dispute reinvestigation (`dispute_reinvestigation`) | cond. obligation | `$B query … Reinvestigate` | `O(…)` |
| Adverse-action disclosure (`adverse_action_disclosure`) | cond. obligation | `$B query … DiscloseReportSource` | `O(…)` |
| No obsolete info (`obsolete_information`) | prohibition | `$B query … ReportObsoleteInformation` | `F(…)` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
