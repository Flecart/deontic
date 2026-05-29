# Baseline comparison: with the reasoner vs without

LegalBench's reference baseline is **direct LLM classification** (few-shot prompt
→ label). The pipeline here inserts a **formal kernel**: LLM formalizes the
contract to `.ddl`, then `deontic` decides the label. This documents how to
compare the two and what each buys; running it produces the numbers (the
LegalBench splits are needed and aren't bundled here).

## The two pipelines

| | Without reasoner (baseline) | With reasoner (this repo) |
|--|--|--|
| Steps | text + hypothesis → LLM → label | text → LLM → `.ddl` → `deontic query/abduce` → label |
| Where the answer comes from | the model's weights | a deterministic proof over explicit rules |
| Output | a label (maybe a rationale) | label **+** the firing rules / minimal facts (`--trace`, `abduce`) |
| Failure mode | hallucinated/inconsistent labels, no audit trail | mis-formalization (wrong atoms/arrows) — but *inspectable* |
| Consistency | same contract can flip across hypotheses | one theory answers all hypotheses coherently |

## What the kernel changes

- **The inference step stops being the hard part.** Once a contract is in DDL,
  the label is exact and reproducible; two hypotheses about the same clause can't
  get contradictory answers, because they query one shared theory.
- **It moves the error to a checkable place.** A wrong answer is now a wrong
  *rule*, visible in the `.ddl` and the trace — auditable and fixable — rather
  than an opaque model verdict.
- **It does not, by itself, improve raw accuracy.** Accuracy now depends on
  formalization fidelity (the LLM's NL→DDL step). The win is auditability,
  consistency, and the `[JUDGE: …]` signal when the contract is genuinely
  ambiguous — not a free accuracy boost.

## Protocol to get numbers

For each task split (`contract_nli_*`, then `cuad_*`, …):

1. **Without:** few-shot prompt the LLM with (contract, hypothesis) → predicted label. Record accuracy vs gold.
2. **With:** prompt the LLM (via `prompts/law-to-ddl.md`) to emit a `.ddl` for the contract; run `deontic` for each hypothesis (`query` for obligations/prohibitions, `abduce 'P(x)'`/`'C(x)'` for permissions/classifications); map derivable→Entailment, opposite-derivable→Contradiction, neither→NotMentioned. Record accuracy vs gold.
3. **Also measure, for the With pipeline:** formalization fidelity (human spot-check of the `.ddl`), abstention rate (`[JUDGE: …]` / NotMentioned), and agreement between the two pipelines.

Expected shape of the result: comparable or slightly lower raw accuracy for the
kernel pipeline, but far higher *consistency* and a full audit trail — the trade
this project is built around.

## Status

- `contract_nli/` — 14 tasks formalized (entailment) + 3 NLI-label variants; the
  kernel returns the designed label for all (see `contract_nli/BASELINE.md`).
- `cuad/` — representative CUAD clause types formalized the same way (in progress).
- Numbers for steps 1–3 above: **pending dataset access**.
