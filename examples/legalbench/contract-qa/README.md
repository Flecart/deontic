# LegalBench contract_qa — deontic yes/no questions as DDL

Yes/no questions about a contract (employment/services) that turn on a duty or
permission. (`B=./.lake/build/bin/deontic`, project root.)

| Question (file) | Clause type | Test | Result | Answer |
|-----------------|-------------|------|--------|--------|
| Notice before resigning? (`notice_before_resign`) | cond. obligation | `$B query … GiveTwoWeeksNotice` | `O(…)` | YES |
| Terminate at will? (`at_will_termination`) | permission | `$B query … TerminateAtWill` | `Ps(…)` | YES |
| Must pay overtime? (`overtime_pay`) | cond. obligation | `$B query … PayOvertime` | `O(PayOvertime)` | YES |
| Barred from disclosing secrets? (`confidentiality_duty`) | prohibition | `$B query … DiscloseEmployerSecrets` | `F(…)` | YES |
| Must reimburse approved expenses? (`expense_reimbursement`) | cond. obligation | `$B query … Reimburse` | `O(Reimburse)` | YES |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
