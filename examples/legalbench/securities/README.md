# LegalBench securities — federal securities-law duties as DDL

Core deontic securities-law duties. (`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| Insider trading (`insider_trading`) | prohibition | `$B query … TradeOnMNPI` | `F(…)` |
| Tipping (`tipping`) | prohibition | `$B query … TipMNPI` | `F(…)` |
| Reg FD (`reg_fd`) | cond. obligation | `$B query … PublicDisclosure` | `O(…)` |
| §16 reporting (`section16_reporting`) | cond. obligation | `$B query … ReportOnForm4` | `O(…)` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
