# LegalBench can-spam — CAN-SPAM Act duties as DDL

Core CAN-SPAM duties of commercial-email senders.
(`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| No false header (`false_header`) | prohibition | `$B query … UseFalseHeaderInfo` | `F(…)` |
| No deceptive subject (`deceptive_subject`) | prohibition | `$B query … UseDeceptiveSubject` | `F(…)` |
| Opt-out mechanism (`opt_out_mechanism`) | obligation | `$B query … ProvideOptOutMechanism` | `O(…)` |
| Honor opt-out (`honor_opt_out`) | cond. prohibition | `$B query … SendCommercialEmail` | `F(…)` |
| Physical address (`physical_address`) | obligation | `$B query … IncludePhysicalAddress` | `O(…)` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
