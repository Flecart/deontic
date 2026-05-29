# LegalBench fair-housing — Fair Housing Act duties as DDL

Core FHA duties of housing providers and agents.
(`B=./.lake/build/bin/deontic`, project root.)

| Duty (file) | Clause type | Test | Result |
|-------------|-------------|------|--------|
| No refusal (`no_refusal`) | prohibition | `$B query … RefuseOnProtectedBasis` | `F(…)` |
| No discriminatory terms (`discriminatory_terms`) | prohibition | `$B query … ImposeDiscriminatoryTerms` | `F(…)` |
| No discriminatory ads (`discriminatory_advertising`) | prohibition | `$B query … MakeDiscriminatoryAdvertisement` | `F(…)` |
| No steering (`no_steering`) | prohibition | `$B query … SteerOnProtectedBasis` | `F(…)` |
| Reasonable accommodation (`reasonable_accommodation`) | cond. obligation | `$B query … ProvideReasonableAccommodation` | `O(…)` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
