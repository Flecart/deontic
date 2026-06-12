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
Across four grounder families: the program collapses from 100% to base rate
the moment an instance is unlisted (true-atom recall 100→0); closed
descriptions fall 8–40 points across novelty tiers; open descriptions stay
flat (e.g. 88.7→84.2 for gpt-4.1) and beat closed at Tier 2 for every family
(+13 to +25 points), at an interpretation cost of ~$0.002 per case. Three
second-order findings sharpen the thesis: extension-size sweeps show drafting
effort buys in-distribution accuracy but essentially zero OOD coverage; the
strongest reasoning model widens the rules-vs-standards gap (literalism makes
enumerations more brittle, and makes unverifiable intensions ungroundable —
repaired measurably by local evidentiary redrafts); and every verdict error
in ~6,000 evaluation rows is a grounding error, none a deduction error, with
the formal layer contributing zero paraphrase variance. We report honestly
where the bill lands: converting flat atom-level accuracy into verdicts pays
a compounding tax that naive staged grounding does not fix, so strong models'
holistic judgments currently beat their own naive grounded pipelines at the
verdict layer — the conversion layer, not the predicate layer, is the open
problem.

## 1. The inversion

A statute drafted in the 1950s prohibits "vehicles in the park," and seventy
years later it governs e-scooters its drafters could not have imagined. Hart
named the property that makes this possible *open texture*: the predicates of
law do not carry their extensions with them; "vehicle" is bound to concrete
instances not at drafting time but at application time, by an interpreter
facing the case. Four decades of AI & Law has treated this property as the
field's principal obstacle — you cannot formalize "reasonable," so
formalization stalls at the closed-textured fragment (tax schedules, benefit
formulas), which is precisely where Rules-as-Code and smart contracts live
today.

We argue the obstacle framing has it backwards. Open texture is not a defect
that formalization must eliminate; it is **law's generalization mechanism** —
a deliberate deferral of concept-binding from drafting time to application
time. A rule that enumerates its instances is bound at drafting time and
generalizes exactly as far as its drafter foresaw. A standard that states a
purpose defers binding, and therefore reaches instances from worlds that did
not exist when it was written. The reason deferral was an obstacle for
machine-readable norms is mundane: deferred binding requires a competent
interpreter present at application time, and until now there wasn't one.

Kaplow's rules-vs-standards economics makes the trade precise: rules are
specified ex ante (cheap to apply, brittle to the unforeseen); standards
acquire content ex post at adjudication (robust, but each application costs an
interpretation). Where a legal system should sit on that spectrum is governed
by the cost of ex-post interpretation. LLMs collapse that cost by orders of
magnitude — from a tribunal hearing to a fraction of a cent — which moves the
optimum, for machine-readable norms, sharply toward the standard end. The
question is whether anything is lost in the move. Handing the whole norm to
the LLM loses what made formalization attractive: determinism, auditability,
verifiable conflict resolution. The contribution of this paper is to show that
nothing forces that bundle: the norm can be factored so that deferral buys
generalization while the formal layer keeps verification.

## 2. The factorization

The architecture splits the norm at the joint Hart identified — between its
*structure* and its *predicates*:

- **The skeleton is formal and closed.** Rules, exceptions,
  exceptions-to-exceptions, superiority, obligation vs permission vs
  prohibition, violation versus compensation, directed bearers: all of it is
  encoded in defeasible deontic logic (Governatori-style proof theory,
  implemented in Lean 4) and computed deterministically, with replayable proof
  certificates. LLM discretion cannot touch this layer.
- **The predicates are open-textured.** Atoms are opaque tokens; each carries
  a mandatory natural-language description — the atom's *contract*. The LLM's
  entire role is the penumbra problem in its smallest form: *does this fact
  situation fall under this described concept?* — a local classification task,
  the thing LLMs are demonstrably good at. Errors stay local (one atom, one
  description, one case), auditable (the certificate names exactly which atom
  assignments drove the verdict), and reparable by editing one description or
  accreting one precedent — never by retraining or rewriting the system.

This resolves the conditional that makes "let an LLM interpret the law" sound
reckless. We do not need LLMs to *judge cases* — weigh, balance, decide. We
need them to *classify instances under described concepts*: a strictly weaker
demand, isolated by the architecture, and measurable per-atom. The experiment
below measures exactly that, with the deduction layer held provably fixed
(every verdict error in 864 evaluation rows is a grounding error; zero are
deduction errors).

## 3. Related work

The gap this work occupies is easiest to state per cluster (full survey with
links: `docs/RELATED.md`).

**LLM + formal-engine pipelines.** The shape "LLM grounds facts, solver
decides" now exists in several monotonic variants on human tax law: LLM+Prolog
on SARA (arXiv:2508.21051, the closest pipeline), multi-agent statutory
formalization (arXiv:2509.00710), logic-grounded guideline QA
(arXiv:2510.01530). All are monotonic — no defeasibility, exceptions,
superiority, compensation, or bearers — and all work on human statutes, where
contamination is unmeasurable. Most telling: SARA's statutes were *edited to
be unambiguous*. The open-texture problem is defined away rather than studied;
none of these works treats definition openness as a variable.

**Rule-application benchmarks.** SARA, RuleArena (arXiv:2412.08972), τ-bench
(arXiv:2406.12045) and its red-teaming extensions measure an *agent's*
adherence to crisp rules stated in NL. None separates the interpreter role
from the decision role, none scores grounding apart from deduction, none
varies how concepts are defined. LogiSafetyBench (arXiv:2601.08196) is the
closest *benchmark-construction* relative — formal spec as oracle, synthesized
cases, gold by construction — but with LTL safety properties, crisp
constraints, and the LLM as regulated agent rather than interpreter.

**Open texture and LLMs.** The interpretation literature discusses LLMs in
the penumbra (survey arXiv:2603.05392; Judge Newsom's concurrences
experimenting with LLM readings of "landscaping" are the real-world anecdote),
and Hartian positivism has been proposed as an alignment frame
(arXiv:2410.17271). What does not exist is a controlled benchmark that varies
*definition openness* (intensional vs extensional) against *instance novelty*
and measures generalization. The Rules-as-Code literature explicitly
speculates LLMs "may be of some assistance … although detailed testing will be
necessary." This paper is that test.

**Norm societies, AI courts, agent commerce.** LLM-society work produces
either emergent conventions without a formal layer (GovSim, naming games) or
policy prompts the agent self-judges (τ-bench style); courtroom simulations
(AgentCourt, AgentsCourt) predict verdicts of human courts holistically, with
no replayable theory. Agent-payment infrastructure (x402, AP2) can prove *what
happened* but not *what was owed* — its own roadmaps name dispute resolution
as the missing layer; Kleros outsources exactly our penumbra problem to staked
human crowds at human speed. We instantiate the missing piece these literatures
point at from both sides: a verifiable normative layer whose open-textured
predicates are interpreted by machine at machine speed.

## 4. Experimental design

### 4.1 The statute

An inter-agent personal-data transfer statute (`eval/expA/statute.ddl`): 8 rules
over 7 groundable atoms, with the structures that distinguish defeasible deontic
logic from monotonic encodings — a default permission (r0), a default
prohibition with a two-step compensatory chain (r1: O¬share ⊗ notify ⊗
compensate), exceptions (consent r2, anonymization r5), exceptions-to-exceptions
(revocation r3 defeats consent; certification r7 defeats the commercial
prohibition r6), and a duty that overrides prohibitions (emergency r4), wired by
a 15-pair superiority relation. Verdict space: status of `share` ∈ {obligatory,
permitted, forbidden}; for cases where the hand-off already happened, also
violation and whether the notify remedy is owed. A deliberately deontic detail:
breaches of r3/r6 are violations *without* a notify duty (no compensation chain
attaches to them) — an engine-computed distinction a holistic judge must
reconstruct in prose. We are the legislator: in the target setting (norms for
AI agent societies) owning the vocabulary is the design point, not a
simplification.

### 4.2 Two bindings of the same norm

Each atom carries two descriptions. *Closed* — a best-faith extensional
enumeration of drafting-time instance categories ("a consent form signed by the
subject; an opt-in checkbox …"). *Open* — the purpose-stated intension ("clear
affirmative agreement, in any form that demonstrates it, by the subject or an
empowered delegate"). The closed enumeration is additionally compiled, with no
LLM anywhere, into the **program arm**: a lookup from structured record fields
to atoms — an executable smart contract that is *exactly* the drafting-time
extension. Rules and superiority are identical across regimes; texture is the
only manipulated variable. Gold atom truth is defined by the intension (the
legislator's meaning).

### 4.3 Novelty tiers

Tier 0: instances listed in the closed enumerations. Tier 1: unlisted
near-variants of listed categories (a passport number where "government-issued
identification number" is listed; an e-signed release where "signed consent
form" is listed). Tier 2: post-drafting world shift — instances satisfying the
intension while falling outside *every* listed category: gait-signature
profiles, smart-meter occupancy traces, consent issued by the subject's
empowered delegate agent, revocation broadcast by the subject's agent,
attestation via trusted execution environments or zero-knowledge compliance
proofs. Hart's no-vehicles penumbra, manufactured under lab conditions.

### 4.4 Backward generation, gold by construction

A latent truth assignment over the 7 atoms is sampled under world-coherence
constraints (revocation presupposes a grant; a grant and de-identification
presuppose person-level content); the engine computes the gold verdict from the
true atoms (replayable via `--why` proof certificates); each true atom is
instantiated with a bank item of the case's tier plus negative-bank distractors
for 1–2 false atoms; a **third-family narrator** (claude-sonnet-4.6; grounders
are OpenAI/DeepSeek/Qwen) renders a ~160-word pre-verdict review memo. A
tier-aware leak check rejects narrations containing atom names, statute
vocabulary stems, or 5-grams of the open description (always) or the closed one
(at tiers 1–2; Tier-0 instances echo the drafted categories by design).
Generation is audited, and the audit has teeth: it caught three world-model
defects (incoherent distractor composition, ungroundable adjacent-matter
emergencies, consent-without-subject worlds) that were fixed and regenerated
before the headline run — each defect manifested as a *grounder being right
where our gold was wrong*.

### 4.5 Arms, metrics, validations

Arms: **oracle** (gold atoms → engine; harness check), **program** (closed-id
lookup → engine; no LLM), **ground_closed** / **ground_open** (LLM classifies
the 7 atoms from the memo under neutral labels C1..C7 — the regimes differ
only in definition text — then the engine decides), **staged_closed/open**
(one dedicated call per atom), **holistic** (LLM reads the English statute with
open definitions + memo, outputs verdict/violation/remedy directly), and
**ground_closed@K** (closed definitions truncated to K categories; the
extension-size sweep). Metrics: atom-level true-recall and false-positive rate
by regime×tier (primary), verdict accuracy by arm×tier, violation+remedy
accuracy on the acted subset, paraphrase flip-rate across narration variants,
tokens per case. Hard validations before reading any result: oracle = gold on
every case; program = 100% at Tier 0; balanced verdict classes; zero leak
flags.

## 5. Results

Predictions P1–P5 were registered before any LLM run (git history). The
micro-pilot (Stage 1c: 72 cases × 12 arms/models = 864 rows, zero parse
errors; all validations green — oracle 100% everywhere, program 100% at Tier
0 with true-atom recall exactly 100/0/0) gives:

### 5.1 The generalization curve (P1, P2 — confirmed)

Atom-level accuracy (all 7 atoms × 24 cases per tier):

| binding | tier 0 | tier 1 | tier 2 | Δ(0→2) |
|---|---|---|---|---|
| program (no LLM) | 100% | 33% | 33% | −67 |
| closed + gpt-4.1 | 93.5% | 78.6% | 71.4% | −22.1 |
| closed + deepseek | 95.2% | 73.8% | 61.9% | −33.3 |
| **open + gpt-4.1** | **88.7%** | **89.3%** | **86.3%** | **−2.4** |
| **open + deepseek** | **83.9%** | **83.9%** | **81.0%** | **−2.9** |

The Kaplow crossover is exactly where theory puts it: enumeration wins
in-distribution (closed > open at Tier 0 by ~5–11 points), the intension wins
out-of-distribution (open > closed at Tier 2 by ~15–19 points), and the
no-LLM program — the smart contract — collapses to base rate the moment any
instance is unlisted, by pure under-inclusion (true-atom recall 0%). Both
model families replicate the pattern.

### 5.2 Where errors land matters more than how many (the verdict layer)

Verdict accuracy converts atom accuracy through the flip set, and the
conversion is unforgiving: open+gpt-4.1's flat ~88% atom accuracy yields only
62–75% verdicts (≈0.88^k compounding), while closed's Tier-2 *verdict*
accuracy (79%) exceeds open's despite far worse atom recall — closed's
misses are correlated and frequently land outside the flip set. Two
structural findings explain the residuals:

- **Gist vs artifact atoms.** Closed enumerations of *scenario-type* atoms
  generalize by category gist (emergency Tier-2 recall 11/16, revoked 18/18
  — a new kind of emergency still reads as an emergency); *artifact-type*
  enumerations do not (certified 0/26, personal_data 11/38, anonymized 3/16
  at Tier 2). Open texture bites hardest where extensions are artifact-like.
- **Epistemic-bar atoms.** The open `anonymized` intension ("no person *can*
  be re-identified") demands an unobservable guarantee; grounders rightly
  refuse to affirm it from a memo (recall 2/2/0 of 8). Where verification
  is impossible at application time, the standard loses to the operational
  rule — Kaplow's verification-cost condition, visible per-atom.

Naive per-atom staged grounding (one call per atom) does **not** fix the
conversion (staged_open ≈ ground_open everywhere): the postmortem's full
prescription (engine-computed criticality, flip-set targeting) remains open
work, and we report the negative result.

### 5.3 Holistic ≈ open+engine (P3)

In the pilot, the end-to-end judge (English statute + memo) tracks the open
grounded arm within noise at every tier (gpt-4.1: 71/67/58 vs 75/67/62) —
both are interpretation-limited. At Stage 2 scale this equivalence holds for
the two weaker families but **breaks for the two strongest** (§5.5): the
formal layer's benefits are not free at the verdict layer under naive
grounding. What does hold unconditionally: every error in every row of every
run is a grounding error; none is a deduction error (oracle rows exact
throughout).

### 5.4 Repair is local and it works at the predicate layer

- **Closed regime, precedent accretion**: appending decided Tier-2 instances
  ("as held in prior decisions: …") from half the Tier-2 cases repairs
  **18/22** previously-missed true atoms on held-out cases, with 2 new
  breaks and **zero** Tier-0/1 verdict regressions. (Net verdict movement in
  the small eval slice was zero — the fixed atoms sat outside the flip
  sets; the claim, like the headline, lives at the atom layer.)
- **Open regime, evidentiary redraft**: re-drafting the two pathological
  intensions (anonymized, emergency) to judge described *process and claim*
  rather than unobservable fact — still enumeration-free — lifted deepseek
  verdicts 58→75 (t0) / 58→67 (t1) and gpt-4.1 modestly; the anonymized
  residual traced to a narrator composition defect (transformed-form
  framing), fixed before the main run.

Both repairs are one-line description edits with measured, bounded blast
radius — the operation a holistic judge does not possess.

### 5.5 The main run: four model families, 288 paired cases

The headline replicates at scale (287 memo cases after leak exclusion; oracle
exact on all; program 100 / 34.7 / 35.4). Tier-2 atom-level accuracy, by
grounder:

| grounder | closed | open | gap |
|---|---|---|---|
| deepseek-v4-flash | 61.3% | 76.2% | +14.9 |
| gpt-4.1 | 67.9% | 84.2% | +16.3 |
| qwen3.6-plus | 70.5% | 83.6% | +13.1 |
| gpt-5.4 | 55.4% | 80.1% | +24.7 |

Open beats closed at Tier 2 for **every** family, and the open curves are flat
across tiers for every family (e.g. gpt-4.1: 88.7/87.7/84.2;
gpt-5.4-with-redrafts: 82/82/82). The naive capability prediction (P4: Tier-2
accuracy slopes up with model strength) is **not** supported — and the truth
is better: the strongest reasoning model (gpt-5.4) has the *lowest* closed
score and the *largest* gap. Reasoning models read enumerations most
literally; **literalism widens the rules-vs-standards gap**. The same
literalism punishes unverifiable intensions: gpt-5.4 grounds open `emergency`
at 9% and `anonymized` at 10% recall (near-zero false positives everywhere) —
the §5.2 epistemic-bar pathology, scaled up by model strength. One round of
evidentiary redrafting lifts these to 22%/39% and flattens its atom curve at
82% — repair is iterative, local, and measurable, but necessity-style
intensions remain hard for literalist graders.

**The verdict layer is the honest tax.** At Stage 2 scale the two strongest
models do *better* reading the whole English statute holistically than
through naive batched grounding (gpt-5.4: 83/73/75 holistic vs 42/38/44
grounded-open; qwen: 87/72/78 vs 73/64/70). The pilot's "factorization costs
nothing" does not survive scale at the verdict layer: compounding (~0.84^k)
plus flip-set placement currently prices the factorization's auditability at
some verdict accuracy for strong models. The conversion layer — engine-guided
criticality, burden-of-proof defaults, precedent caching — is the open
engineering problem, and naive per-atom staging is already ruled out (§5.2).

**Leakage control (narrated-variant).** Re-rendering the same cases as
outcome-scrubbed tribunal FACTS sections lifts *all* arms uniformly (+4.5 to
+5.6 points) — formal register is simply clearer. No holistic-specific
genre-leakage advantage exists when narratives are outcome-free by
construction; the FOIA-style leakage pathway requires outcome-bearing prose,
which backward generation eliminates.

**Variance decomposition.** Across paraphrase pairs, all LLM arms flip
21–35% of verdicts; `program` and `oracle` flip **0%** by construction. The
formal layer contributes zero variance; all variance is interpretation —
which is what makes atom-level precedent caching (freeze an interpretation
once made) the natural determinism mechanism.

**Violation and remedy (P5).** On the 120 acted cases, grounded-closed
attributes violation/notify-duty at 88–91%/87–93% vs holistic's 71–83%/68–78%
(better for 3 of 4 families; program: 87/90). The deontic distinctions the
engine computes for free — breach-without-notify-duty for r3/r6 — are
precisely where holistic prose reasoning slips.

## 6. The economics figure

Kaplow's trade-off, measured on the same statute:

- **Ex-ante (drafting) cost does not buy OOD coverage.** Truncating the
  closed enumerations to their first K categories (gpt-4.1, 288 cases):
  K=2 → Tier-0 atom acc 83%, Tier-2 67%; K=4 → Tier-0 90%, Tier-2 69%;
  K=full → Tier-0 92%, Tier-2 68%. Doubling and redoubling the enumeration
  buys ~9 points in-distribution and **~1–2 points out-of-distribution**:
  the Tier-2 curve is flat in K. No feasible amount of drafting catches the
  e-scooter, because Tier-2 instances are outside the listed *categories*,
  not merely the listed instances.
- **Ex-post (interpretation) cost is collapsed.** Deferred binding costs
  ~650–780 tokens per case per grounder (≈ $0.002 at gpt-4.1 prices,
  ≈ $0.0002 at deepseek prices) and ~2 seconds. The interpreter whose absence
  made open texture an obstacle now costs five orders of magnitude less than
  the institution it replaces at this step (a human determination).

Where the optimum sits on the rules–standards spectrum is set by these two
curves; the second one just moved.

## 7. What the generator iterations teach (method, not embarrassment)

Three defects were caught by per-atom audit between pilot and headline run,
and each followed the same signature: *a grounder being right where our gold
was wrong*. (i) Distractor composition: an "anonymization done badly" negative
attached to a non-personal dataset made the narrator imply quasi-identifiers
gold denied. (ii) Adjacent-matter emergencies: urgency items narrated as
separate requests correctly failed the open definition's necessity test —
emergency banks were re-bound to the requested dataset. (iii)
Consent-without-subject worlds: grounders inferred personhood from consent
evidence, exposing a missing world constraint (a grant presupposes a data
subject). The lesson generalizes: when gold is synthesized from latent
worlds, *grounder–gold disagreement concentrated on one atom is a world-model
bug detector*. Benchmarks built without this loop ship these bugs as "model
errors."

## 8. Threats to validity

- **Strawman risk (closed baseline).** The closed enumerations were authored
  as best-faith operationalizations, and the data shows they are not straw:
  closed beats open at Tier 0 and its scenario-type categories generalize to
  Tier 2 (emergency 11/16, revoked 18/18). The collapse is selective and
  structural (artifact-type atoms), not an artifact of weak drafting.
- **Tier-2 novelty is heterogeneous.** "Distance from the extension" varies
  by atom; for scenario-type atoms our Tier-2 instances remain
  gist-recognizable. The per-atom tables expose this rather than averaging
  over it; claims should be read atom-wise.
- **Narrator effects.** Leakage is measured (n-gram + stem checks; zero
  flagged narrations in the headline runs) and the narrator is a third model
  family; but residual composition artifacts (the §7 catalogue) bound the
  absolute numbers — they are symmetric across regimes, so the closed-open
  *gap* is robust to them.
- **Ecological validity.** The domain is synthetic and we are the legislator.
  That is the target regime (norms for AI agent societies), not a
  convenience: vocabulary ownership is exactly what an institution designer
  for agent commerce has, and synthetic gold-by-construction is what makes
  contamination measurement unnecessary rather than impossible.
- **Scale and scope.** One statute, 7 atoms, 3-class verdicts, 56 coherent
  worlds; two grounder families in the pilot (four in the main run).
  Single-bearer; the engine's multi-bearer machinery is unexercised here.
- **Headroom.** Frontier grounders may saturate Tier 2 eventually; the
  capability sweep (P4) is designed so that *that result would itself be the
  thesis* — the interpreter got good enough — while the weak-model regime
  shows the curve.

## 9. Conclusion

Law's open-textured predicates are not an obstacle to formalization but its
generalization mechanism: they defer concept-binding to application time.
LLMs make that deferred binding cheap — we measure ~$0.002 per case — and a
defeasible deontic skeleton keeps it consistent and auditable: zero deduction
errors, zero structural variance, replayable certificates, violation and
remedy semantics that holistic judges measurably fumble. Factored this way,
norms generalize where fully-specified rules cannot: the no-LLM program dies
on the first unlisted instance, enumerations decay with novelty no matter how
long the drafter's list, and the purpose-stated intension holds flat across
worlds its drafter never saw — for every model family we tested, with the gap
*widening* under the most literal-minded frontier model. What is not yet
solved is the conversion layer: turning flat predicate-level accuracy into
verdict-level accuracy without paying the compounding tax. The architecture
points at its own remedy — the engine knows each case's flip set, burdens of
proof are defeasible-logic natives, and atom-level precedent caching converts
interpretation into accreting case law — and that, not predicate
interpretation, is where the engineering frontier now sits.
