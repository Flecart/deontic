# Experiment B results — the commons statute (S2)

288 narrated cases (claude-sonnet-4.6 narrator, memo style, seed 2, 48
assignments × 2 variants × 3 tiers), zero leak-flagged. Arms: oracle, program,
ground_closed, ground_open, holistic × {gpt-4.1, gpt-5.4, deepseek-v4-flash,
qwen3.6-plus}; extras: ground_closed@2/@4 + ground_open2 (gpt-4.1),
ground_open2 (gpt-5.4), holistic_closed (gpt-5.4, qwen3.6-plus). Validation
gates green: oracle = gold on all 288 cases (assertion-checked), program
100/35.4/35.4 verdict with true-atom recall exactly 100/0/0.

## Headline: the texture effect replicates on a second statute

Tier-2 atom-level accuracy, open−closed gap, case-clustered bootstrap
(2,000 resamples):

| grounder | closed | open | gap [95% CI] |
|---|---|---|---|
| deepseek-v4-flash | 58.5 | 74.1 | +15.6 [+11.8, +19.6] |
| gpt-4.1 | 78.3 | 89.6 | +11.3 [+8.8, +14.1] |
| gpt-5.4 | 64.4 | 82.6 | +18.2 [+14.9, +21.6] |
| qwen3.6-plus | 79.9 | 85.4 | +5.5 [+2.8, +8.0] |

All four gaps positive, all CIs clear of zero (cf. expA: +13.1 to +24.6).
Open curves are flat-or-rising across tiers for every family (gpt-4.1:
87.9/86.5/89.6); closed decays for every family (gpt-5.4: 98.4/84.2/64.4).
Program collapses 100 → 35.4 at the first unlisted instance; oracle exact
everywhere; program/oracle paraphrase flip-rate 0% vs 19–47% for all LLM arms.

## Pre-registered texture-profile check (README table): 5/7 right, 2 wrong

Pooled closed-regime Tier-2 true-atom recall:

| atom | predicted | observed | verdict on prediction |
|---|---|---|---|
| allocation_granted | artifact: collapse | 38.3% | ✓ |
| over_quota | artifact: collapse | 46.1% | ✓ |
| priority_certified | artifact: collapse | 62.0% | partial (≈expA revoked level) |
| grant_suspended | scenario: survives | 72.7% | ✓ |
| offset_posted | epistemic bar | closed 23.1, open 55.6 | ✓ (both depressed, open higher) |
| contention | scenario: survives | **38.0%** | ✗ — collapses |
| essential_workload | scenario-ish | **28.8%** | ✗ — collapses |

The two misses are informative: `contention` ("the pool cannot serve all
entitled demand") and `essential_workload` (necessity test) are *system-state
/ counterfactual* predicates — the verifiability axis dominates the
artifact/scenario axis when the intension asserts something about the whole
world rather than about an exhibited artifact or event. gpt-5.4 grounds open
`contention` at 63/24/11% recall across tiers (near-zero false positives:
23 FP / 972 false-atom slots) — the same epistemic-bar literalism expA found
on `emergency`/`anonymized`, now on a second statute.

## Extension-size sweep (gpt-4.1): a gist dividend at small K, then flat

| K | tier 0 | tier 2 |
|---|---|---|
| 2 | 80.5 | 66.8 |
| 4 | 98.4 | 77.7 |
| full (3–8) | 98.2 | 78.3 |

Unlike expA (T2 flat in K throughout), the first few *diverse* categories buy
real Tier-2 accuracy (+10.9 from K=2→4): with only two categories the model
reads the enumeration literally; four diverse examples teach the *gist*
("exceeding any stated cap"), which generalizes. Beyond K=4 the curve is flat
(+0.6), and the full enumeration still sits 11.3 points below the
zero-enumeration intension (89.6). Refined cross-statute claim: enumerations
generalize exactly as far as their gist abstracts; drafting longer lists past
the gist threshold buys ~0 OOD.

## Evidentiary redrafts (open2): repair works, but examples re-import closure

gpt-5.4 true-atom recall (T0/T1/T2), open → open2:

- essential_workload 40/38/55 → **52/62/70** (the expA emergency repair
  replicates);
- offset_posted 62/98/52 → 92/95/**32**: the redraft names example forms
  ("depositing reserve capacity, a confirmed top-up purchase, a transferred
  share"), which fixes Tier 0 and *hurts* Tier 2 — the strict reader treats
  the examples as a closed list. **Evidentiary redrafting by example is
  itself a move toward the rule end of the spectrum**; redrafts must state
  evidence *kinds* (recorded, escrowed, sized-to-cover), not instance forms.

Net gpt-5.4 atom curve: open 87.8/82.7/82.6 → open2 90.6/84.1/79.9.

## Verdict layer: the conversion tax is domain-dependent

| arm (T0/T1/T2 verdict) | gpt-4.1 | gpt-5.4 | qwen | deepseek |
|---|---|---|---|---|
| ground_closed | 97.9/76.0/49.0 | 96.9/84.4/51.0 | 99.0/89.6/54.2 | 90.6/61.5/38.5 |
| ground_open | 79.2/76.0/81.2 | 69.8/64.6/66.7 | 90.6/88.5/81.2 | 62.5/61.5/65.6 |
| holistic | 67.7/58.3/65.6 | 90.6/80.2/80.2 | 86.5/81.2/76.0 | 61.5/60.4/69.8 |
| holistic_closed | — | 93.8/81.2/61.5 | 91.7/82.3/71.9 | — |
| program | 100/35.4/35.4 | | | |

Unlike expA (holistic > grounded-open for the two strongest models), on expB
grounded-open ≥ holistic at Tier 2 for 3 of 4 families (gpt-4.1 +15.6, qwen
+5.2, deepseek −4.2, gpt-5.4 −13.5). With ~3.6 true atoms/case on average and
~85–90% atom accuracy, compounding is milder here; the expA conversion tax is
real but not universal. holistic_closed decays with tier exactly like
grounded closed (93.8→61.5; 91.7→71.9) while open holistic holds — the
pipeline-independence control replicates.

Violation/remedy (acted n=114): grounded arms 72–88% report-duty accuracy vs
holistic 75–85%; program 75/79 (its misgrounding now also misfires the
remedy chain — under-inclusion makes it miss violations, unlike expA where
closed-id lookup carried the acted subset).

## Bank validation + one audit-loop catch

Two annotator families judged all 92 bank items against the open intensions,
standalone (`bank_validation.jsonl`): gpt-5.4 87/92, qwen3.6-plus 82/92.
One disagreement was *not* annotator literalism: both families held that a
**lapsed voucher** satisfies "at some point granted … an entitlement covering
this category" — and they were right; the drafted intension was missing
temporal scope. Fixed before any grounding run ("…that covers this category
of draw **and the period of the draw**"); targeted re-validation: gpt-5.4
14/14 on the atom. The remaining disagreements are strict-reader false
negatives on system-state predicates (contention, essential_workload) — the
same epistemic-bar boundary the grounding results then exhibited. The audit
loop works on the *drafting* side too: independent validation is a
mis-drafted-intension detector, not only a world-model bug detector.

## Artifacts

`cases_memo.jsonl` (288, 0 flagged), `results_main.jsonl` (4,032 rows),
`results_extras.jsonl` (864), `results_open2_gpt54.jsonl` (288),
`results_holclosed.jsonl` (576), `bank_validation.jsonl` (184),
`RESULTS_main_tables.md` (full scorer output), `bootstrap_ci.py` output above.
Dry-run gates: `cases_dry.jsonl`, `results_dry.jsonl`.

## Persuasion probe (advocacy narration)

288 re-narrations of the same cases (`cases_advocacy.jsonl`, seed-paired with
the memo set, zero leak-flagged): identical facts plus the requesting team's
3-4 sentence pro-draw position statement (recharacterize/stress/minimize
only; no new facts — gold unchanged by construction). **Attack success** =
among cases with gold=forbidden where the arm was correct on the neutral
memo, the fraction flipped to permitted/obligatory by rhetoric alone
(`sway.py`; oracle and program pin the 0% floor by construction):

| family | holistic | ground_closed | ground_open |
|---|---|---|---|
| gpt-5.4   | 12.0% | **0.0%** | 4.3% |
| qwen3.6-plus | 9.1% | 7.4% | 7.4% |
| gpt-4.1   | 9.6% | 12.1% | 13.5% |
| deepseek-v4-flash | 14.3% | 17.1% | 17.9% |

Findings: (i) the factorization's persuasion resistance is
**capability-dependent** — for the strongest model the grounded arms are
nearly immune (0%/4.3% vs 12% holistic; its net sway under advocacy is even
slightly *negative*, i.e. it grows more conservative when argued at), while
for weak models rhetoric penetrates at the atom layer itself
(deepseek grounded ≈ 17-18% > its holistic) — narrowing the question does
not by itself immunize a grounder that can be talked out of a factual
classification; (ii) raw accuracy under advocacy is NOT the right metric:
the position statement recaps the facts (helping weak models) and pushes
toward the majority side of the verdict prior, so several arms' accuracy
*rises* under attack — the conditioned attack-success rate is the honest
number; (iii) `program`/`oracle` 0% confirms the harness.
