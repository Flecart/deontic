# LegalBench maud — merger-agreement deontic covenants as DDL

The deontic deal points from the Merger Agreement Understanding Dataset:
interim covenants, no-shop, efforts, and the fiduciary-out permission.
(`B=./.lake/build/bin/deontic`, project root.)

| Deal point (file) | Clause type | Test | Result |
|-------------------|-------------|------|--------|
| Ordinary-course covenant (`maud_ordinary_course`) | obligation | `$B query … ConductOrdinaryCourse` | `O(…)` |
| Reasonable best efforts (`maud_reasonable_best_efforts`) | obligation | `$B query … UseReasonableBestEfforts` | `O(…)` |
| No-shop (`maud_no_shop`) | prohibition | `$B query … SolicitCompetingOffers` | `F(…)` |
| Fiduciary out (`maud_fiduciary_out`) | permission carve-out | `$B abduce … 'P(ChangeRecommendation)' --all` | `{ SuperiorProposal }` |
| No financing condition (`maud_financing_condition`) | prohibition | `$B query … RefuseToCloseForLackOfFinancing` | `F(…)` |
| Hell-or-high-water (`maud_hell_or_high_water`) | obligation | `$B query … TakeAntitrustActions` | `O(…)` |
| MAE termination (`maud_mae_termination`) | permission carve-out | `$B abduce … 'P(TerminateForMAE)' --all` | `{ MaterialAdverseEffect }` |

See [`../COMPARISON.md`](../COMPARISON.md) for the baseline protocol.
