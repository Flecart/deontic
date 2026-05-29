# LegalBench fdcpa — Fair Debt Collection Practices Act duties as DDL

Core FDCPA debt-collector prohibitions and duties formalized as DDL.
(`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| No unusual-time contact (`unusual_time_calls`) | prohibition | `$B query … CommunicateAtUnusualTime` | `F(…)` |
| No harassment (`harassment`) | prohibition | `$B query … HarassConsumer` | `F(…)` |
| No false representations (`false_representation`) | prohibition | `$B query … UseFalseRepresentation` | `F(…)` |
| Validation notice (`validation_notice`) | cond. obligation | `$B query … SendValidationNotice` | `O(…)` |
| Cease on request (`cease_communication`) | cond. prohibition | `$B query … ContactConsumer` | `F(ContactConsumer)` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
