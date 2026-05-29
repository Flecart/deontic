# LegalBench supply_chain_disclosure — SB 657 disclosure duties as DDL

The five mandatory disclosures under the CA Transparency in Supply Chains Act
(SB 657), each a disclosure obligation of a covered retailer.
(`B=./.lake/build/bin/deontic`, project root.)

| Disclosure (file) | Clause type | Test | Result |
|-------------------|-------------|------|--------|
| Verification (`verification_disclosure`) | cond. obligation | `$B query … DiscloseVerificationEfforts` | `O(…)` |
| Audits (`audit_disclosure`) | cond. obligation | `$B query … DiscloseAuditPractices` | `O(…)` |
| Certification (`certification_disclosure`) | cond. obligation | `$B query … DiscloseCertificationRequirement` | `O(…)` |
| Internal accountability (`internal_accountability_disclosure`) | cond. obligation | `$B query … DiscloseAccountabilityStandards` | `O(…)` |
| Training (`training_disclosure`) | cond. obligation | `$B query … DiscloseTrainingPractices` | `O(…)` |

All conditioned on `CoveredRetailer`. See [`../COMPARISON.md`](../COMPARISON.md).
