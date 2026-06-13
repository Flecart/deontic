# Experiment D results — agency & delegation (S4, the large multi-bearer rung)

288 narrated cases (claude-sonnet-4.6, seed 4, 48 assignments × 2 variants ×
3 tiers); 8 leak-flagged excluded → 280 scored. Arms: oracle, program,
ground_closed, ground_open, holistic × {gpt-4.1, gpt-5.4, deepseek-v4-flash,
qwen3.6-plus} (4,032 rows). Gates green: oracle = gold on all 288; program
100% honor at Tier 0 with true-atom recall exactly 100/0/0. Honor verdict is
near-binary (majority baseline ≈ 50%); headline claims stay at the atom and
the structural levels.

## Finding 1 — the size axis: holistic verdict degrades, grounded+engine holds

This is expD's reason to exist (12 rules, exception depth 5 vs 8 rules in
A/B). **Grounded+engine honor-verdict accuracy is statute-size-invariant**
(the per-atom interpretation task does not change with rule count); **holistic
accuracy is not.** Tier-2 honor verdict, holistic minus grounded_open, across
statute sizes:

| model | A (8 rules) | B (8 rules) | **D (12 rules)** |
|---|---|---|---|
| gpt-4.1           | −10 | −16 | −3 |
| gpt-5.4           | +31 | +14 | +18 |
| deepseek-v4-flash | +4  | +4  | −2 |
| qwen3.6-plus      | +8  | −5  | **−32** |

The sharpest datapoint is qwen: holistic-competitive on the 8-rule statutes
(78/76% Tier-2), it **collapses to 48.9% — the binary chance baseline — on the
12-rule statute**, while its grounded+engine pipeline holds at 80.4%. It can
no longer resolve a depth-5 exception chain in prose. gpt-4.1 holistic is
likewise low and flat (64–66%), well under its grounded arms at Tier 0 (95%
closed). The pre-registered prediction (verdict tax inverts with statute
size) **holds for the models that have a tax to begin with**; the strongest
model (gpt-5.4) again resists, holding 80% holistic — the same
capability-exception seen in the literalism (RQ3) and persuasion findings.
Honest summary: *deep normative structure is where moving the deduction into
a verified engine stops being a tax and starts being a rescue — for every
model except the strongest.*

## Finding 2 — multi-bearer: the engine computes a second bearer's duties for free

The suite's first directed-multi-bearer statute: the honor question lands on
`@Principal`, conduct duties (`disclose ⊗ disgorge` for conflicted dealing)
on `@SubAgent`. Sub-agent conduct-duty breach detection (engine-mediated arms
only — the engine computes it from grounded atoms; a holistic verdict has no
such output to score):

| arm | breach acc |
|---|---|
| ground_closed (4 families) | 88.2 – 94.6% |
| ground_open (4 families)   | 86.4 – 95.7% |
| program (no LLM)           | **48.2%** |
| oracle                     | 100% |

Grounded+engine attributes the second bearer's breach at ~90%; the no-LLM
program fails (48% — its under-inclusion misses the `revoked`/`self_dealing`
predicates that trigger the conduct duty), and a holistic judge produces no
separable sub-agent verdict at all. The directed-obligation machinery
flagged "unexercised" in the A/B write-up now carries a clean result: the
factorization gives a per-bearer audit the holistic arm structurally cannot.

## Finding 3 — texture gap is moderate here, and that is consistent (RQ3)

Atom-level Tier-2 accuracy, open − closed (open arm = the `within_scope`-fixed
re-grounding, see below):

| model | closed | open | gap |
|---|---|---|---|
| deepseek-v4-flash | 74.9 | 84.1 | +9.2 |
| gpt-4.1           | 78.1 | 82.2 | +4.1 |
| gpt-5.4           | 76.9 | 84.5 | +7.6 |
| qwen3.6-plus      | 80.4 | 86.7 | +6.2 |

Positive for all four but **smaller than A/B** (+5–25). Consistent with
the RQ3 refinement: this statute's predicates are mostly scenario-type
(`mandate_revoked`, `ratified`, `self_dealing`), epistemic-bar
(`counterparty_good_faith`, `urgent_necessity`) and system-state, with low
artifact-type concentration — and the texture gap is concentrated in
artifact-type atoms. Notably, the closed enumerations here generalize to
Tier 2 *well* (76–81%), because the artifact atoms that collapse on A/B
(certificates, data-type lists) have few analogues in agency law. expD thus
supports the headline's *direction* on a third statute while sharpening the
claim: the magnitude of the texture effect is a function of how
artifact-like the predicates are, which varies by legal domain.

## Bank validation + an audit catch (within_scope underspecified)

gpt-5.4 84/92 (91.3%), qwen3.6-plus 87/92 (94.6%) agreement vs the open
intensions — in line with A/B. The audit loop caught a real drafting defect
(see `NOTES_within_scope.txt`): the `within_scope` open intension said
"judged by the purpose the mandate serves" without naming that purpose, so
gpt-5.4 over-read (a billboard campaign "fits a brand-promotion mandate") and
qwen under-read (won't confirm catalogue items without seeing the mandate).
Both trace to one ambiguity. Fixed by naming the procurement/supply domain
(still enumeration-free); re-validation: **every within_scope disagreement eliminated** (both
annotators agree on all 15 items). Aggregate 84/92 (gpt-5.4), 90/92 (qwen);
gpt-5.4 flat because its disagreements relocate to the epistemic-bar atoms.

**This is the thesis in microcosm.** Re-grounding under the fixed intension
(narration unchanged, only the description) lifted `within_scope` open
true-recall from 52/54/63% to **99/97/98%** across tiers and the open arm's
atom accuracy by 2–5 points (e.g. gpt-5.4 80.5/79.3/81.1 → 85.6/82.1/84.5),
*widening* the Tier-2 texture gap to +4.1…+9.2. The same fix barely moved the
closed arm (closed `within_scope` recall 61/29/8 → 68/26/14, since the
enumeration was already explicit). An open intension is only as good as its
specification: an under-specified standard under-grounds, and repairing it
— without adding a single enumerated instance — recovers the generalization.
The honor-verdict and holistic numbers are unaffected (the size-axis and
multi-bearer results are from the verdict layer, which `within_scope`'s atom
flag barely shifts: qwen holistic 48.9% vs grounded-open 80.4% is identical
before and after). **All atom-level open numbers in this file use the fixed
re-grounding (`results_reground.jsonl`); verdict/holistic/program use
`results_main.jsonl`.**

## Artifacts

`cases_memo.jsonl` (288, 8 flagged), `results_main.jsonl` (4,032 rows),
`bank_validation.jsonl` (184), `RESULTS_tables.md` (full scorer output).
Statute: `statute.ddl` (engine-verified, 9 doctrinal worlds + chains).
