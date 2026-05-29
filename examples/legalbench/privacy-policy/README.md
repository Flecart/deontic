# LegalBench privacy_policy — deontic data-protection duties as DDL

Privacy-policy questions about *duties and rights* (notify, delete, provide
access, share) formalized as DDL. (`B=./.lake/build/bin/deontic`, project root.)

| Question (file) | Clause type | Test | Result | Answer |
|-----------------|-------------|------|--------|--------|
| Notify users of a breach? (`breach_notification`) | cond. obligation | `$B query … NotifyUsers` | `O(NotifyUsers)` | YES |
| Delete data on request? (`data_deletion`) | cond. obligation | `$B query … DeleteData` | `O(DeleteData)` | YES |
| Provide access on request? (`access_right`) | cond. obligation | `$B query … ProvideAccess` | `O(ProvideAccess)` | YES |
| May share with providers? (`third_party_sharing`) | permission carve-out | `$B abduce … 'P(ShareData)' --all` | `{ ServiceProviderPurpose }` | YES |
| Delete after retention? (`data_retention`) | cond. obligation | `$B query … DeleteAfterRetention` | `O(…)` | YES |
| Children's data collection barred? (`childrens_data`) | prohibition | `$B query … CollectChildData` | `F(…)` | YES |
| Marketing only with consent? (`marketing_consent`) | permission carve-out | `$B abduce … 'P(SendMarketing)' --all` | `{ MarketingConsent }` | YES |
| Must implement security? (`security_measures`) | obligation | `$B query … ImplementSecurity` | `O(…)` | YES |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
