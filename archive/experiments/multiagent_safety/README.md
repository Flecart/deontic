# Multi-agent AI safety with the deontic engine — experiment package

A set of experiment designs to show that the **deterministic defeasible-deontic
reasoner** improves *multi-agent AI safety*. Five experiments stand on the
engine's **pure deduction over a fixed, pre-specified statute** — *no judge in
the loop*; the only learned component is **grounding** (scenario → atoms), a
perception step. A sixth adds a **judge** (LLM adjudication + evolving case law)
to show the contrast and the residual safety guarantees when a judge is fallible.

Each file gives: **design · dataset (source, or an implementable generation
recipe) · baseline(s) · evaluation**.

## What "without / with judging" means here

The repo's `caselaw/` work uses a **judge** — an oracle or LLM that supplies a
verdict on each case, which an institution then accumulates into law (`caselaw/
llm_judge.py`, `institutions.py`). The engine can also *flag* an unresolved
conflict (`[JUDGE: …]`) for a human to resolve.

- **Without judging (Exp 1–5):** the statute is **authored up front and frozen**.
  The engine only *computes* `O`/`F`/`P`/violation/deadlock from grounded facts.
  No model resolves conflicts; no rulings are learned. Exp 2 *detects* the
  `[JUDGE]` deadlock and uses it as a **stop/abstain** signal — detection is not
  adjudication, so it still counts as "without a judge."
- **With judging (Exp 6):** an LLM judge adjudicates incidents live; an evolving
  case-law corpus + a small inviolable constitutional floor govern a commons.

This split isolates the claim. If we can show safety wins with a *frozen* statute
(no judge to second-guess), the engine's value rests on **verifiable deduction**,
not on a model's verdicts — the strongest version of the safety argument.

## The five "no-judge" experiments, by safety property

| # | Safety property (AI-safety theme) | Mechanism used | Builds on |
|---|---|---|---|
| 1 | **Harm prevention without adjudication** — a deterministic shield keeps a commons safe vs selfish/adversarial agents | `query`/`check`: `F` + `+∂_⊥` violation as an action filter | `caselaw/commons_loop.py`, `prosocial-agents` |
| 2 | **Safe failure / calibrated abstention** — refuse-and-escalate on genuine norm conflicts instead of confabulating | `[JUDGE]` deadlock detection (`engine.has_unresolved_conflict`) | `eval/` unresolved items, `caselaw` T10 |
| 3 | **Specification-gaming red-team** — find rulebook loopholes *before* agents exploit them | `abduce` over statutes (backward search) | `Deontic/Abduce.lean`, `eval/tools/backward_gen.py` |
| 4 | **Adversarial-manipulation robustness** — grounded deduction is invariant to peer-agent reframing that flips an LLM | grounding + frozen engine; self-consistency | `eval/` paraphrase/distractor flags |
| 5 | **Emergent multi-agent harm** — individually-compliant agents whose *joint* action is unsafe; correlative-rights clashes | directed obligations `@Bearer`, per-bearer scoping | `examples/clauses/enterprise_saas_msa.ddl` |

Exp 6 (with judge): **scalable oversight under a fallible/captured judge** — a
constitutional floor pins safety violations to ~0 while case law adapts.

## Design principles shared across the package

- **Hold the base model + grounding prompt fixed across arms** — we test
  *deduction/enforcement*, not retrieval (per `docs/evaluation.md`).
- **The engine is the gold oracle** where labels are needed (work backwards:
  config → engine verdict → narrate), reusing `eval/tools/backward_gen.py`.
- **Report where the engine does *not* help** — single-rule caps need no logic
  (F1 in `caselaw/REPORT.md`); the wins must come from depth, conflict, and
  composition. Be honest about the grounding ceiling (split grounding error from
  deduction error in every measured arm).
- **Cost is a denominator** — tokens + latency the engine step adds, per result.

## Honesty / threats (apply to all)

- A neuro-symbolic system is only as right as (a) the encoded theory and (b) the
  grounding; a wrong theory makes the engine *confidently* wrong. Every
  experiment reports **grounding accuracy separately** — it bounds the ceiling.
- Don't score the engine against `tests.sh` — those are the theory's own outputs
  (circular). Use independent vignettes with externally-known answers.
- Fact spaces in the controlled arms are small/enumerable; claims are exact
  *there* but small-scale (cf. `caselaw/REPORT.md` §Threats).

## Files

- [`exp1_enforcement_shield.md`](exp1_enforcement_shield.md)
- [`exp2_calibrated_abstention.md`](exp2_calibrated_abstention.md)
- [`exp3_abduction_redteam.md`](exp3_abduction_redteam.md)
- [`exp4_adversarial_robustness.md`](exp4_adversarial_robustness.md)
- [`exp5_compositional_bearers.md`](exp5_compositional_bearers.md)
- [`exp6_with_judge_caselaw_floor.md`](exp6_with_judge_caselaw_floor.md) — *with judge*
