# LegalBench ada — Americans with Disabilities Act duties as DDL

Core ADA duties of covered entities. (`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| No disability discrimination (`no_discrimination`) | prohibition | `$B query … DiscriminateOnDisability` | `F(…)` |
| Reasonable accommodation (`reasonable_accommodation`) | cond. obligation | `$B query … ProvideReasonableAccommodation` | `O(…)` |
| Accessibility (`accessibility`) | obligation | `$B query … RemoveBarriersWhereReadilyAchievable` | `O(…)` |
| Interactive process (`interactive_process`) | cond. obligation | `$B query … EngageInteractiveProcess` | `O(…)` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
