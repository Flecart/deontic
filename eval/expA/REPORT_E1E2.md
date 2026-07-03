# E1 + E2 on expA: precedent-augmented grounding and dispute-selected accretion

First full run of the common-law experiments (docs/plan_common_law.md §2),
2026-07-03. Everything below is a count over committed JSONL logs
(`results_e1.jsonl`, `results_e2.jsonl`, `disputes_e1.jsonl`,
`store_precedent.jsonl`, `store_uniform.jsonl`); score tables reproduce with
`e1_score.py` / `e2_score.py`.

## Setup

- **Stream**: 200 backward-generated cases (`gen_stream.py`, seed 0), 24 latent
  assignments all recurring under fresh narrations (claude-sonnet-4.6
  narrator), tier mix 72/62/66 (T0/T1/T2), 0 leak-flagged.
- **Dispute detection**: gpt-4.1 + deepseek-v4-flash ground each case
  precedent-free (open descriptions, neutral C1..C7 labels); a case is
  *contested* iff their **engine verdicts** diverge (outcome-level dispute, the
  Priest–Klein filing condition — unknown atoms alone are logged, not
  triggers).
- **Adjudicator**: claude-sonnet-5 (thinking on), retrieval over the store so
  far (k=5, embed); it issues per-condition findings + a reuse-oriented
  rationale; the verdict is always the engine's on its findings. 114 calls,
  680k tokens. A matched-size uniform store (same judge, same accretion clock,
  uniformly drawn cases) was built alongside.
- **E1 eval**: 3 cheap grounders (gpt-4.1, deepseek-v4-flash, glm-4.7) × 10
  arms × 200 cases against the frozen stores, as-of-t retrieval. **E2**: same
  grounders on the last 60 cases; stores of size n ∈ {2,5,10,20,39} selected
  from the first 140 cases by five accretion policies, gold-labeled holdings
  except where noted.

## E1 findings

**F1 — the static frontier replicates on the stream.** Program collapses
(100/19/32% by tier), closed decays (e.g. deepseek 96/74/44), open is flat but
weak (53–68% overall). Note open is weaker here than in the stage-2 static
banks — the single batched 7-atom grounding call plus the unknown→false
conversion penalize it; treat cross-suite comparisons with care.

**F2 — precedent beats the same open statute, and beats uniform examples at
matched store size** (pooled over 3 models, case-clustered bootstrap 95% CIs):

| comparison | pooled acc | Δ | 95% CI |
|---|---|---|---|
| precedent@embed vs ground_open | 67.8 vs 62.0 | **+5.8pp** | [+1.2, +10.7] |
| precedent@embed vs uniform (matched n) | 67.8 vs 62.0 | **+5.8pp** | [+1.8, +9.8] |
| goldfs (ceiling) vs ground_closed | 84.0 vs 74.8 | **+9.2pp** | [+4.0, +14.0] |
| goldfs vs precedent@embed | 84.0 vs 67.8 | **+16.2pp** | [+11.0, +21.5] |

The lift is capability-dependent: largest for the weakest grounder
(deepseek +13.0pp overall), smallest for glm-4.7 (+1.5) — precedent
substitutes for capability, echoing the stage-2 factorization finding.

**F3 — the ceiling clears the frontier; the adjudicated arms do not (yet).**
`goldfs` (gold-relevant, gold-labeled shots) beats *both* static poles at every
tier (81–88% overall). The proposed gate (X≥70% of the closed↔open T0/1 gap
closed, Y≥90% of open's T2 advantage kept) is **not met** by the adjudicated
arms at store=57/k=5 (X spans −33..+133% across model×mode cells, noisy at
last-tercile cell sizes). The 16.2pp goldfs−precedent gap decomposes into the
two engineering targets below (retrieval, holding quality). Mechanism
validated; current instantiation under-tuned.

**F4 — epistemic coordination: shared precedent aligns distinct models.**
Mean pairwise Cohen's κ on verdicts:

| arm | early | mid | late |
|---|---|---|---|
| ground_open | 0.542 | 0.658 | **0.448** |
| ground_closed | 0.635 | 0.568 | 0.565 |
| precedent@embed | 0.743 | 0.776 | **0.788** |
| precedent@rule | 0.737 | 0.735 | **0.794** |
| goldfs | 0.773 | 0.877 | 0.817 |

Open drafting *diverges* over the stream; precedent arms converge — the
plan's coordination claim, with a positive slope. (Uniform examples also raise
κ, to 0.73 — some of the effect is "any shared conditioning"; selection adds
accuracy on top, F2 and E2.)

**F5 — retrieval is a measured bottleneck, and legal similarity ≠ narrative
similarity.** Gold relevance = shared latent assignment. P@5 / hit@5 on rows
with ≥1 relevant precedent available: gold retrieval 73%/100%; embed cosine
11%/42%; **atom-overlap 27%/82%**; rule-subsumption 13%/45%. Embedding the
narration retrieves *narratively* similar cases — the COLIEE Task-1 problem
reproduced with gold labels. Atom-overlap nearly doubles relevant-hit rate yet
does **not** raise verdict accuracy over embed (63–71 vs 66–69): with noisy
holdings, better retrieval surfaces more wrong labels too — retrieval and
holding quality are complements, not substitutes.

**F6 — Priest–Klein diagnostics.** Dispute rate 28.5% (57/200), roughly flat
across tiers (28/26/32%). Selection concentrates on the boundary: first-pass
accuracy drops from 69.9% on settled to 56.1% (gpt-4.1) and 14.0% (deepseek)
on contested; the sonnet-5 judge itself is only 54.4% verdict-exact (75.7%
atom-exact) on contested cases. Win shares are asymmetric — the judge sided
with gpt-4.1 in 49/57 disputes, deepseek 5, neither 3 — the predicted
Priest–Klein deviation under asymmetric party capability. Governance reading:
**in an agent society, the stronger party disproportionately writes the
precedent.**

## E2 findings (selection at matched store size)

Verdict accuracy on the 60-case tail, pooled over 3 models, gold-labeled
holdings:

| policy | n=2 | n=5 | n=10 | n=20 | n=39 |
|---|---|---|---|---|---|
| dispute | 74.4 | 81.7 | 88.3 | 91.7 | **94.4** |
| oracle (error-sampling ceiling) | 70.6 | 87.2 | 88.3 | 91.7 | 90.6 |
| uniform | 71.7 | 83.3 | 87.2 | 91.1 | 87.2 |
| recency | 78.9 | 86.7 | 91.1 | 89.4 | 86.7 |
| dispute_adj (judge-labeled) | 74.4 | 81.1 | 72.8 | 72.2 | 76.1 |

**F7 — litigation is active learning.** Dispute-selected accretion is
monotone in n and best at scale: at n=39 it beats uniform by +7.2pp and even
edges the oracle error-sampling ceiling. Agreement tells the same story:
dispute κ rises monotonically 0.668→**0.899** (highest everywhere at n≥10),
while recency peaks at n=10 and decays — old cases go stale; disputed cases
stay on the boundary.

**F8 — the adjudicator-noise tax caps the system.** Identical selection,
different labels: gold vs sonnet-5 holdings are indistinguishable at n≤5,
then diverge by **+15.6 to +19.4pp** at n≥10 — noisy law doesn't merely help
less, it flatlines (~72–76%) while clean law climbs to 94.4%. This is E4's
error-entrenchment risk quantified early, and it matches E1's 16.2pp
goldfs−precedent gap: ~46% of accreted holdings carry a verdict differing
from gold (judge is 54.4% on contested — contested cases are *hard*).

## What this means for the program

1. **Both plan hypotheses survive contact**: precedent conditioning beats the
   static frontier when labels are right (F3), and dispute selection beats
   uniform sampling at matched size (F7) — the two load-bearing claims of the
   common-law architecture, each with CIs clear of zero at the pooled level.
2. **The binding constraint is holding quality, not retrieval alone** (F5 ×
   F8). Next engineering moves, in order of expected value: (a) adjudicator
   verdict quality — self-check pass, higher-k retrieval for the judge,
   or panel adjudication; (b) hybrid retrieval (atom-overlap ∘ embed);
   (c) store growth beyond 57 (T=300+ streams, more statutes).
3. **Law-and-economics texture is real in silico**: boundary concentration,
   asymmetric win shares under asymmetric capability, staleness of recency —
   all classic selection-literature phenomena, reproduced with
   gold-by-construction ground truth.

## Limitations

One statute (expA), 3 cheap grounders, one narrator (shared-narrator confound
as in stage 2), one judge; E2 evaluates a 60-case tail with nested store
prefixes (no reshuffled replicates yet); k=5 fixed everywhere; the dispute
pair is capability-asymmetric (deepseek's 14% contested accuracy makes it
close to a noise party — rerun with a matched pair before claiming the win-
share number as a general result); gate cells at last-tercile×tier are small
(n≈25–41). The E1 open-arm level is not comparable to stage-2 numbers
(batched vs staged grounding).
