# LegalBench telemarketing_sales_rule — FTC TSR duties as DDL

Core FTC Telemarketing Sales Rule duties/prohibitions formalized as DDL.
(`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| Do-Not-Call (`do_not_call`) | prohibition | `$B query … CallDNCNumber` | `F(CallDNCNumber)` |
| Calling hours (`calling_hours`) | prohibition | `$B query … CallOutsidePermittedHours` | `F(…)` |
| Identification (`caller_identification`) | obligation | `$B query … DiscloseIdentityAndPurpose` | `O(…)` |
| Robocall consent (`robocall_consent`) | permission carve-out | `$B abduce … 'P(Robocall)' --all` | `{ PriorExpressWrittenConsent }` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
