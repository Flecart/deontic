# Project positioning & open decisions

Shared project memory — the strategy and open questions that are *not*
derivable from the code. Checked into the repo so every machine and every
agent session starts from the same picture. Update this file when a decision
here changes; keep it short.

## Paper strategy (pivoted 2026-07-02 — supersedes the same-day AI&Law plan)

**One paper: "Common law for agent societies."** Thesis: ship norms for agent
societies as a *process, not a text* — thin open-textured statute +
accumulated precedent + formal coherence monitor — and show it beats every
static drafting (closed / open / hybrid) on epistemic coordination,
behavioral coordination, and robustness. Primary audience: agents / MAS
(AAMAS, COINE, ML agents tracks); AI & Law secondary.
**Full brief: `docs/plan_common_law.md` — read it before touching `eval/`,
`freight/`, or `paper/`.**

Role changes vs the superseded plan: expA–F becomes the motivating static
frontier (the impossibility that justifies the mechanism); `freight/` is
promoted from future work to the society-level experiment (E3); `[JUDGE]`
adjudication moves *in scope* (E1's adjudicator exercises it).

Claim discipline that survives the pivot:

- Precedent-based reasoning becomes claimable once E1 stores real holdings —
  but still **do not claim human-style "analogical reasoning"**; the
  mechanism is retrieval + conditioning, and the paper says so.
- The expB redraft finding stays load-bearing: refinement must stay
  **intensional**, not extensional — now tested directly as E4's
  amendment-policy arm.
- The machine-legislator point stands: the system designer is the
  legislator, so shared vocabularies, stipulated priority, and
  gold-by-construction evaluation are legitimate.
- Welfare is never reported without coherence (freight pilot lesson).

## Repo cleanup record (2026-07)

Real-law-practice material was removed from the tree to match the framing;
everything is recoverable from annotated tags:

- `codice-penale-final` — the full Italian penal code example
  (`examples/codice_penale`, 754 articles, 105-assertion tests).
- `real-law-final` — `examples/legalbench`, the LegalBench three-condition
  harness (`eval/run.py` etc.), `archive/` (caselaw + pre-pivot experiments).
- Branch `human-case-law-11-june` — the UK FOIA/EIR tribunal corpus, frozen
  and deliberately unmerged. It contains Lean core work main lacks (directed
  `@Party` abduce goals in `Abduce.lean`/`Parser.lean`) that should be
  cherry-picked separately someday; note main's own abduce-priority fix
  (`37390c7`) conflicts with it.

## Open design question: Lean-native DDL (opened 2026-05-27)

Should the project go "everything in Lean" instead of the runtime `.ddl`
parser? Three independent moves were framed: (1) a `ddl%` macro for in-Lean
theories, (2) `Decidable` + `native_decide` per-theory proven verdicts,
(3) a verified engine + soundness metatheory (Proposition 1).

Load-bearing facts: the engine uses `partial def`, which is unprovable —
verification needs a total fixpoint (fuel-indexed or `OrderHom.lfp`), likely
pulling in Mathlib (currently avoided); `−∂`/team-defeat need
strong-negation/stratified treatment, so move (3) is research-grade. The
product purpose (LLM formalizes norms → engine reasons → LLM interprets)
makes the runtime parser the integration boundary — keep it regardless.
Standing recommendation: do moves (1)–(2) when ergonomics matter, scope (3)
separately. Still open; `docs/architecture.md` lists machine-checked
refinements as future work.
