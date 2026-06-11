# Open Texture as a Generalization Mechanism: Defeasible Deontic Skeletons with LLM-Interpreted Predicates

*Angelo Huang — draft, June 2026. Experiments in `eval/expA/`; engine in `Deontic/` (Lean 4).*

## Abstract

Forty years of AI & Law treats open texture — Hart's "no vehicles in the park" —
as the obstacle to formalizing norms: you cannot enumerate at drafting time what
"vehicle" will mean at application time, so formalization stalls, and the systems
that do get built (smart contracts, Rules-as-Code) formalize only the
closed-textured fragment. We invert the claim: open texture is not a formalization
bug but **law's generalization mechanism** — a deliberate deferral of
concept-binding from drafting time to application time, which is why a 1950s
statute still applies to e-scooters. Deferred binding was an obstacle only because
it requires a competent interpreter at application time, and we did not have one.
Now we do. We factor machine-readable norms at exactly that joint: a **formal
defeasible deontic skeleton** (exceptions, superiority, violation-vs-compensation,
bearers — computed deterministically, with proof certificates) over
**open-textured atoms** (opaque tokens whose mandatory natural-language
description is their contract; an LLM's only job is the local classification
"does this fact situation fall under this described concept?"). On a synthetic
inter-agent data-transfer statute with gold labels by construction and novelty as
a controlled variable, we measure the generalization curve of the same norm under
three bindings — program (drafting-time, no LLM), closed descriptions + LLM,
open descriptions + LLM — against a holistic LLM judge and an oracle ceiling.
[RESULTS SUMMARY PLACEHOLDER]

## 1. The inversion

[Hart's open texture; Schauer. Standard AI&Law treatment: obstacle. The
inversion: deferral of concept-binding = the mechanism by which written norms
survive unforeseen worlds. Kaplow's rules-vs-standards economics: rules bind
ex ante (cheap to apply, brittle), standards bind ex post (costly to apply,
robust); position on the spectrum is set by the cost of ex-post interpretation.
LLMs collapse that cost. Smart contracts are stuck at the rule end; our
factorization lets machine-readable norms move toward the standard end without
giving up mechanical application.]

## 2. The factorization

[The architecture splits the norm at the right joint: skeleton formal and
closed (engine: Governatori-style defeasible deontic logic in Lean 4; proof
certificates; LLM discretion cannot touch it) — predicates open-textured
(atoms opaque; description = contract; grounding = local classification; errors
stay local, auditable, fixable by adding a rule). The conditional this resolves:
we do not need LLMs to judge cases, only to classify instances under described
concepts — strictly weaker, isolated, measurable.]

## 3. Related work

[Condensed from docs/RELATED.md — keep the Δ structure:
- LLM+formal-engine pipelines (Tax/Prolog arXiv:2508.21051, multi-agent
  formalization arXiv:2509.00710): monotonic, human law, no open-texture
  variable — SARA edits statutes to be unambiguous, defining the problem away.
- Rule-application benchmarks (SARA, RuleArena, τ-bench): crisp rules, agent
  adherence; no interpreter/decision split, no novelty tiers.
- Open texture + LLMs: discussed (surveys, Judge Newsom's anecdote), proposed
  as alignment frame (arXiv:2410.17271); no controlled benchmark varies
  definition openness × instance novelty. This is the free square.
- Norm societies / AI courts / agent-commerce infra: conventions without
  verification or verdicts without theory; x402/AP2 prove what happened, not
  what was owed; Kleros outsources the penumbra to human crowds.
- Rules-as-Code essay explicitly calls for "detailed testing" of LLMs vs open
  texture — this paper is that test.]

## 4. Experimental design

### 4.1 The statute
[8 rules, 7 groundable atoms, defaults/exceptions/exception-to-exceptions,
superiority web, one compensation chain (notify ⊗ compensate); single bearer.
Engine-verified probe table. We are the legislator: vocabulary is ours — the
agent-society setting makes this legitimate rather than a simplification.]

### 4.2 Two bindings of the same norm
[closed = best-faith extensional enumeration (also compiled, without any LLM,
into the program arm's lookup — the smart contract); open = purpose-stated
intension. Same skeleton; texture is the only manipulated variable. Gold truth
is the intension (the legislator's meaning).]

### 4.3 Novelty tiers
[Tier 0 = instances listed in the closed enumeration; Tier 1 = unlisted
near-variants of listed categories; Tier 2 = world-shift instances satisfying
the intension outside every listed category (gait signatures, delegated-agent
consent, TEE attestation...). The e-scooter case, manufactured under lab
conditions.]

### 4.4 Backward generation, gold by construction
[latent assignment → engine verdict (certificate) → bank instantiation →
third-family narrator (claude-sonnet-4.6) with leak check: no atom names, no
statute vocabulary, no 5-gram overlap with the open description ever, nor with
the closed one at tiers 1–2. PIMMUR unawareness: narrator ≠ grounder families.]

### 4.5 Arms and metrics
[oracle / program / ground_closed / ground_open / holistic; neutral C1..C7
labels so regimes differ only in definition text. Metrics: verdict acc by
arm×tier (primary at atom level), per-atom true-recall, violation+remedy acc
on acted subset, tokens/case. Validations that must pass before reading
results: oracle=100% everywhere; program=100% at Tier 0.]

## 5. Results

[STAGE 1 + STAGE 2 TABLES PLACEHOLDER
Headline figure: verdict/atom accuracy vs tier, one curve per arm.
Predictions registered before Stage 1:
P1 closed falls Tier 0→2, open ~flat (atom level);
P2 program: 100 → ~base-rate (under-inclusion, deterministic);
P3 holistic ≤ grounded arms on consistency; leakage-free by construction here;
P4 capability scaling: open Tier-2 slopes up with grounder strength, closed flat;
P5 violation/remedy: grounded arms inherit the deontic distinctions (r3/r6
   breaches carry no notify duty) that holistic must reason out in prose.]

## 6. The economics figure

[Extension-size sweep: how many enumerated instances does the closed definition
need to match open's Tier-2 accuracy? + tokens/$ per case by arm: the cost of
deferred binding, measured. Kaplow's trade-off as two curves.]

## 7. Repair (the institutional property)

[Tier-2 failures of the closed regime: minimal fix = add one precedent rule /
one description edit; measure fix rate + regression rate on the full suite.
Contrast: no analogous local operation exists for the holistic judge.]

## 8. Threats to validity

[Closed baseline authored in best faith (strawman risk); Tier-2 novelty
audited (paraphrase risk); narrator leakage measured not assumed; synthetic
domain = contamination-free but ecological validity bounded — the target is
agent societies, where the legislator-owns-vocabulary assumption is real;
single statute; verdict space small; headroom on frontier models.]

## 9. Conclusion

[Thesis sentence. Norms factored as formal-skeleton + open atoms generalize to
unforeseen cases where fully-specified rules cannot, while remaining verifiable
where end-to-end LLM judgment is not.]
