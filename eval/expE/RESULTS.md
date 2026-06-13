# Experiment E results — sale of goods (S3, artifact-heavy rung)

432 cases (72 assignments × 3 tiers × 2 variants), 6 leak-flagged → 426 scored.
3 families (gpt-4.1, deepseek, qwen; no gpt-5.4). Gates green: oracle exact on
all 432; program 100% accept at Tier 0, recall 100/0/0. accept verdict
near-binary (216/210/6).

## The pre-registered "large texture gap" prediction FAILED — and why

Atom-level accuracy is flat and high in BOTH regimes (closed 91/88/89, open
87/87/89; Tier-2 gap −0.3). Diagnosis (honest null, not a bug to hide):
- the two quality standards `conforming` (closed recall 27% even at Tier 0)
  and `merchantable` (37%) are **ungroundable** — they are *relational*
  (item vs. order-spec / trade-norm) and get confounded with co-present
  defects, so a grounder fails them in *both* regimes; there is no gap to
  measure;
- the other 7 atoms' closed enumerations are **abstract enough to
  generalize** ("matches the agreed characteristics" covers novel
  instances), so closed does not collapse.
Lesson (sharpens RQ3): the open>closed gap needs BOTH (a) groundable
predicates and (b) genuinely instance-specific closed enumerations — an
"artifact-type domain" label alone does not produce it.

## The strong result: factorization value at the verdict layer

grounded+engine holds ≈81–91% accept-verdict accuracy across all tiers (Tier-1 dips to ~81),
while holistic falls to 64–76% (gpt-4.1: 76/63/60) and program collapses
100→1. On this 9-rule statute the engine's deterministic deduction rescues
verdict accuracy where holistic prose reasoning fails — the size-axis /
conversion-tax finding, replicated.

## Bank validation (independent annotators)

llama-3.3-70b 100/106 (94.3%), qwen3.6-plus 101/106 (95.3%) vs the open
intensions. Disagreements are scattered penumbra edge cases (silence-as-
acceptance, superset schema), not a systematic ambiguity — no description
edit triggered (the validate-first ordering held cleanly).

Artifacts: cases_memo.jsonl (432, 6 flagged), results_main.jsonl (4,752 rows),
bank_validation.jsonl, RESULTS_tables.md.
