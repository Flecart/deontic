# Project positioning & open decisions

Shared project memory — the strategy and open questions that are *not*
derivable from the code. Checked into the repo so every machine and every
agent session starts from the same picture. Update this file when a decision
here changes; keep it short.

## Paper strategy (decided 2026-07-02)

**One paper. Target community: AI & Law** (ICAIL/JURIX-style), framed as
*law for computer agentic systems*, not law for humans. The multi-agent /
agent-safety community is the secondary audience.

Storyline: GovSim et al. simulate agent societies with no formal
institutions; mechanism-design institutions (CoopEval) are formal but offer
no interpretive flexibility, while intelligent environments keep changing
(agents write tools, spawn sub-environments); prosocial-agents work saw the
gap but governs only the agents you trained. This work imports law's open
texture [Hart] so rules generalize to unforeseen cases: broad initial
principles (do no harm, help humanity) are refined into more precise rules as
new problems emerge in the society.

Claim discipline:

- **Do not claim "analogical reasoning" as mechanism.** The benchmark
  measures *subsumption under a stated intension* — no precedents, no source
  cases (not HYPO/CATO analogy). The intro delimits this explicitly.
- The expB redraft finding is load-bearing: repairing a standard by listing
  example forms fixes Tier 0 and *hurts* Tier 2 — refinement must stay
  **intensional**, not extensional. State it as a design principle.
- The machine-legislator point is a contribution, not an apology: in an agent
  society the legislator is the system designer, so shared vocabularies,
  stipulated priority, and gold-by-construction evaluation are legitimate —
  the first jurisdiction where AI&Law theory is measurable end to end.
- "LLM judges for automatic conflict resolution in open-ended cases" is **not
  yet claimable** — no experiment exercises `[JUDGE]` resolution. The scoped
  version needs a conflict-resolution experiment with meta-principles
  (gold-by-construction superiority) + abstention calibration on genuinely
  underdetermined conflicts. Candidate future work, kept out of the paper.
- `freight/` (emergent case-law agent-society pilot) is the *dynamics* half
  of the story: kept in-tree, cited as research program / future work, not as
  a powered result.

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
