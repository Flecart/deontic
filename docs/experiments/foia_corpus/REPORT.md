# FOIA corpus evaluation report — 84 instances, gpt-4.1

*Run `runs/run_20260611_055806_oracle-ground-llm.jsonl` (2026-06-11). Single
run, default temperature — treat point estimates as ±2–3 instances of run
noise (repeat-seed protocol pending). Model under test: **gpt-4.1**; labels
were drafted by gpt-4.1 too but every label was agent-verified against the
tribunal's stated findings and gated by `verified:` (3 unverified instances
included via `--allow-unverified`, flagged below).*

## The corpus

84 case instances from 67 First-tier Tribunal (GRC) FOIA decisions on Find
Case Law (2025–2026, mostly past model knowledge cutoffs), labelled one agent
per case under [`AGENT_PROTOCOL.md`](AGENT_PROTOCOL.md), selected and
stratified per [`SELECTION.md`](SELECTION.md) (audit trail:
[`candidates.txt`](candidates.txt) — 12 principled exclusions). Part-allowed
decisions are split into per-part instances (8 splits). Coverage: s12, s14,
s21, s23, s24, s26, s27, s30, s31, s35, s36, s38, s40(1), s40(2), s41, s42,
s43, s44, five pure-NCND disputes (`decision: confirm`), multi-exemption depth
cases (up to five stacked), authority-side appeals, and not-held/adequacy
controls. Gold disposition: 61 withhold / 23 disclose → **always-withhold
baseline = 72.6%**.

## Headline results

| arm | disposition | engaged rules | PI direction | facts vs oracle |
|---|---|---|---|---|
| **oracle** (verified facts → engine) | **82/84 (97.6%)** | 83/84 (98.8%) | 41/42 | — |
| **ground** (gpt-4.1 grounds atoms → engine) | 63/84 (75.0%) | 52/84 (61.9%) | 27/42 (64.3%) | **3500/3612 (96.9%)** |
| **llm** (gpt-4.1 decides directly) | 72/84 (85.7%) | 54/84 (64.3%) | 32/42 (76.2%) | — |

Split by gold class (the discriminative subset is *disclose* — the cases where
the authority/ICO position fails, so deference can't fake it):

| arm | withhold-gold (61) | disclose-gold (23) |
|---|---|---|
| oracle | 98.4% | 95.7% |
| ground | 80.3% | **60.9%** |
| llm | 91.8% | **69.6%** |

Cost: 168 OpenAI calls, ~1.17M prompt tokens for the two model arms.

## Findings

1. **The formalization is validated.** Oracle ≈98% across all dimensions: given
   the facts the tribunal found, the 44-rule DDL theory reproduces the
   tribunal's disposition, decisive rule, and PI direction almost perfectly.
   The two oracle disposition misses are *documented* engine limitations, not
   silent errors: the adequacy-of-search control (woodhouse — no rule for
   "search was inadequate" without HoldsInfo) and one unverified NCND
   structural case. The deduction layer is not the bottleneck.

2. **Grounding is the bottleneck — and errors compound through conjunctive
   rules.** The ground arm judges individual atoms at 96.9% accuracy, yet
   exact engagement-set match is only 61.9% and disposition 75.0%. With ~43
   atoms per case, 97% per-atom accuracy still yields ≈1.3 wrong atoms per
   case, and a single false positive (a stray `PiMaintainOutweighs`, a
   spurious prejudice finding) flips the engine's disposition. The engine is
   faithful to its facts; the facts are the failure surface.

3. **Holistic judgment absorbs noise that the engine amplifies — at this
   grounding quality.** llm-only beats ground→engine on disposition (85.7% vs
   75.0%). This *reverses* the n=4 pilot signal and is the honest headline:
   with a strict engine, grounding precision must exceed a threshold before
   the formal layer pays off on outcome accuracy. Note what the engine still
   buys at equal or worse outcome accuracy: every ground-arm verdict carries a
   proof certificate (which rule fired, what it defeated, which facts it
   consumed) and its errors are *attributable* to named atoms — the llm arm's
   72/84 comes with prose.

4. **Both model arms degrade sharply on disclose-gold cases** (ground 60.9%,
   llm 69.6%, vs 92–98% on withhold-gold). llm-only's 85.7% overall is only
   +13 points over the always-withhold baseline (72.6%). The deference
   channel flagged in INDEX.md (the ICO's decision notice is quoted in every
   background) most plausibly explains the asymmetry: agreeing with the prior
   adjudicator is right 73% of the time by construction. The planned `dn`
   baseline arm would quantify this exactly.

5. **Rule selection is hard for everyone** (engaged: ground 61.9%, llm 64.3%
   — exact set match). Common confusions in the logs: asserting the PI atom
   for absolute exemptions, engaging s21 off a published *summary*, engaging
   exemptions the tribunal explicitly bypassed, and missing procedural
   blockers when an exemption is also in play.

## Caveats

- Single run at default temperature; ±2–3 instance noise observed across
  reruns in Phase 0. No repeat-seed averaging yet.
- Engagement scoring is exact-set match — partial credit (per-rule F1) would
  be fairer to both arms and is a one-line scoring change.
- 3 instances are `verified: no` (s23/s24 masking disjunction, one control,
  one inferred s40) and included via `--allow-unverified`.
- Label-drafting used the same model family as the system under test
  (gpt-4.1); drafts were independently verified against tribunal text by
  labelling agents, and the oracle arm's 98% consistency bounds residual label
  noise, but a cross-family drafting pass remains the cleaner protocol.
- DN-in-background leakage is measured only indirectly (finding 4); the `dn`
  arm and a stripped-background regime are specified but not yet run.
- Backgrounds are raw judgment text before the tribunal's reasoning; four
  headingless decisions needed manual cuts (all flagged in case files).

## What this sets up

- **Per-exemption PI atoms** and **partial-credit engagement scoring** before
  the 500-case scale-up.
- The **`dn` baseline arm** to price the deference channel.
- The **atoms-per-call (K) sweep** and **--precedents** ablation now have a
  corpus with enough power: 84 instances × 43 atoms ≈ 3,600 per-atom
  judgments per configuration.
- The grounding-precision threshold (finding 3) is the paper's central
  testable claim: the engine's value on *outcomes* is gated on per-atom
  accuracy; its value on *auditability* is unconditional.
