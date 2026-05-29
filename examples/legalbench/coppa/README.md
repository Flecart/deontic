# LegalBench coppa — Children's Online Privacy Protection Act duties as DDL

Core COPPA operator duties regarding children's personal information.
(`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| Parental consent to collect (`parental_consent`) | permission carve-out | `$B abduce … 'P(CollectChildInfo)' --all` | `{ VerifiableParentalConsent }` |
| Children's notice (`notice`) | obligation | `$B query … ProvideChildrensNotice` | `O(…)` |
| Parental access (`parental_access`) | cond. obligation | `$B query … ProvideChildInfoToParent` | `O(…)` |
| Parental deletion (`parental_deletion`) | cond. obligation | `$B query … DeleteChildInfo` | `O(…)` |
| No conditioning (`no_conditioning`) | prohibition | `$B query … ConditionParticipationOnExcessiveInfo` | `F(…)` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
