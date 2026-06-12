# Constitution texture as a training-time variable (CAI experiment design)

*Design doc, 2026-06-12. Status: awaiting pointer to the user's CAI training
code; everything below is implementable against any RLAIF/DPO-style recipe.*

## Claim under test

The paper measures the rules-vs-standards trade at **application time** (an
interpreter binds the norm's concepts per case). Constitutional AI binds them
at **training time**: a fixed principle list generates preference labels, and
whatever the constitution's texture taught is frozen into the weights. The
open question the paper cannot currently answer: **does the generalization
gap survive distillation into a policy, or does training extract the gist of
an enumeration and flatten it?**

Both outcomes are publishable:

- **H1 (texture survives):** the closed-constitution policy decays on Tier-2
  situations relative to the open-constitution policy → "constitutions
  should be standards" holds at training time; the strongest version of the
  paper's claim, and a direct design input for CAI-style methods.
- **H2 (gist distillation):** training on many Tier-0/1 labeled instances
  teaches the category gist, flattening the gap → RLAIF performs the same
  abstraction the K-sweep's gist dividend shows in-context, which would be
  an important and somewhat surprising result about what preference training
  does to rule lists (and would *weaken* the case against enumerated
  constitutions at training time while leaving the application-time result
  intact).

The K-sweep gist dividend (expB: +10.9 Tier-2 points from 2→4 categories
in-context) makes H2 genuinely live; this is a real experiment, not a
confirmation.

## Design

One factor, two (optionally three) levels — the **constitution's texture**:

- `C-open`: the statute's open intensions, recast as constitution principles
  ("never transfer content that relates to an identified or identifiable
  person without...").
- `C-closed`: the closed enumerations, same recast ("never transfer content
  containing a person's legal name; a residential address; ...").
- optional `C-closed@2`: truncated enumerations (ties the training result
  to the K-sweep).

Everything else identical: same base model, same prompt distribution, same
label budget, same judge recipe, same hyperparameters, same seeds.

### Data generation (reuses the expA/expB machinery wholesale)

1. **Prompts** = situations rendered from latent worlds, exactly like the
   benchmark's memos, but phrased as a *request to the policy model* ("You
   are the holder agent. The recipient asks you to hand over X. Reply with
   your action and reasoning."). Backward generation gives each prompt a
   known latent atom assignment, hence an engine-computed gold action —
   **gold by construction carries over to training data**.
2. **Training prompts draw ONLY Tier-0 and Tier-1 instances** (the
   drafting-time world). Tier-2 instances are *never seen in training* —
   they are the held-out world-shift eval, and contamination is excluded
   because the surface forms are freshly generated.
3. **Preference labels**: judge model + constitution scores response pairs
   (standard CAI). The judge sees only the constitution text — texture is
   the only difference between arms. Judge family ≠ policy family ≠
   narrator family (e.g. judge gpt-5.4 / policy qwen-7B-class / narrator
   claude — adjust to whatever the user's code supports).
4. **Volume**: ~2-4k preference pairs per arm is the standard small-scale
   CAI regime; the generator can produce this in minutes at ~$10-20 of
   narration.

### Training

Whatever the user's code does — DPO or PPO-RLAIF on a LoRA of a small open
model. Both arms must share base checkpoint, data order, and seeds. Two (or
three) adapters out.

### Evaluation

- **Primary**: policy compliance on held-out prompts at all three tiers,
  judged by the engine on the *latent* atoms (we know them — no LLM judge
  needed for the primary metric; the policy's chosen action either matches
  the engine-gold action for that world or not).
- **Secondary**: (a) compliance judged by an independent LLM judge with the
  *open* constitution (the legislator's meaning), to catch actions that are
  literally compliant but purposively wrong; (b) over-refusal rate on
  benign Tier-2-lookalike prompts (negatives bank) — enumerations may
  under-block, intensions may over-block; report both directions; (c) the
  per-atom split (artifact vs scenario vs epistemic-bar) — H1/H2 may
  resolve differently per texture type, which would refine both.
- **Confirmatory comparison**: Tier-2 compliance gap (C-open − C-closed),
  case-clustered bootstrap CI, pre-registered before training.

### Gates (before reading any result)

- Both policies ≥ some compliance floor at Tier 0 (else training failed and
  tier comparisons are meaningless);
- judge sanity: judge+constitution reproduces engine gold on a Tier-0/1
  audit sample at high agreement, for BOTH constitutions (else the label
  channel, not the texture, drives the result);
- the usual leak checks on rendered prompts.

### Confounds to control

- **Length/specificity**: closed constitutions are longer; include a
  token-matched control (pad C-open with neutral preamble) or at minimum
  report token counts.
- **Judge texture interaction**: the judge reading an enumeration may
  produce noisier labels for the same reason grounders do; the judge-sanity
  gate quantifies this — and if label noise *is* the mechanism by which
  closed constitutions lose, that is itself the finding (rule-lists make
  worse training signal), worth reporting as such rather than "controlling
  away."

## What I need from the user

1. Path to the CAI training code (repo + entry point) and what it supports
   (DPO vs PPO; which base models; LoRA?).
2. Compute envelope (local GPU? cloud budget?).
3. Whether the policy domain should be statute A (transfer — reads as a
   safety/privacy constitution) or statute B (commons — reads as an agent
   society institution). A is closer to the CAI framing; B is closer to the
   GovSim narrative. Default recommendation: A.

## Relation to the paper

If run in time: this becomes the headline experiment of the
constitution-framed version ("the rules-vs-standards trade survives — or
doesn't — distillation into weights"), with the current benchmark as the
measurement instrument it rests on. If not: it is the explicitly named next
experiment in the discussion, and the clause-texture annotation of the
Anthropic constitution / OpenAI Model Spec
(`docs/experiments/constitution_texture_annotation.md`) carries the
constitution narrative on its own.
