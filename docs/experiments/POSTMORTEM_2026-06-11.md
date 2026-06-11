# One-pager — why the engine lost to the plain LLM (2026-06-11)

## Experimental setting

Four statute formalizations in defeasible deontic logic, each with a corpus of
real tribunal decisions and verified gold labels (disposition, engaged rules,
PI direction, oracle facts): **FOIA 2000** (120 verified instances, 43-atom
universe), **EIR 2004** (17, 18 atoms), **FA09 Sch 55 tax penalties** (6, 6
atoms), **ERA 1996 unfair dismissal** (3, 5 atoms). Three arms, gpt-4.1,
single run, strict verified-only scoring:

- **oracle** — tribunal-found facts → engine (deduction ceiling);
- **ground** — LLM grounds every atom from the case background (batched
  `--atoms-per-call`), engine deduces;
- **llm** — one holistic call, no engine.

## What we tried

The bet: forcing the decision through a formal layer (atom grounding + proof
calculus) should beat holistic judgment, since per-atom questions are easier
than whole cases. Today we completed the FOIA corpus to 140 case files via
one-agent-per-case labelling with leak control, ran the strict eval on all
domains, ran the first employment eval, and replayed the run log for error
anatomy.

## Results

- **oracle: 146/146 across all domains and dimensions** — every verified gold
  label is consistent with its formal theory. The deductive layer is sound;
  everything below is a grounding problem.
- **The sad part — FOIA: ground 76.7% vs llm 83.3%** on disposition, even
  though ground's per-atom accuracy is **97.2%** (5013/5160).
- Disclose-gold collapse: ground 63.9% / llm 72.2% on disclose-gold cases vs
  82.1% / 88.1% on withhold-gold — both arms ride the ~70% withhold prior.
- Dose-response on atom-universe size: tax (6 atoms) parity, EIR (18)
  **engine wins** 15/17 vs 14/17, FOIA (43) holistic wins. Employment (n=3):
  parity on disposition, engine wins engaged-rules 2/3 vs 1/3.

## Post-experiment analysis (replay of the run log, no new LLM calls)

1. **Errors compound multiplicatively.** Disposition needs ~k≈8 critical
   atoms simultaneously right: 0.97^8 ≈ 0.78 ≈ the observed 76.7%. The
   holistic arm aggregates softly and doesn't multiply.
2. **No graceful degradation: 20 of 28 misses are repairable by flipping ONE
   atom.** Meanwhile disposition hits tolerated up to 5 atom errors — the
   97% uniform per-atom average is the wrong metric; only flip-set atoms
   matter.
3. **21 of 28 misses involve the PI-balance atom.** `PiMaintainOutweighs` is
   not a fact — it *is* the holding — yet we elicit it stripped of decision
   framing, batched with bookkeeping atoms.
4. **The llm arm partly free-rides on leakage** the atom bottleneck discards:
   the ICO decision notice in the background, base rates, and
   *narrative-curation* (judgments are written by the judge, post-decision,
   to make the outcome feel inevitable). Part of llm's edge is genre-reading,
   not reasoning.

## Possible fixes (ranked, with predicted payoff)

1. **Staged, engine-driven grounding** — the engine computes criticality
   (abduce both verdicts, diff the supporting sets): ground posture atoms,
   restrict the universe to claimed exemptions (kills the spurious-atom
   misses), then ask only the live atoms. Lawyer-style issue-spotting,
   computed instead of intuited.
2. **Weight-aware elicitation for dispositive atoms** — dedicated K=1
   full-context call for the PI balance, told the *local* stakes (never
   global priors), with self-consistency voting. The replay says 21/28 misses
   are in its blast radius: fixing half puts ground ≈ 85% > llm 83.3%.
3. **Abstention with role-derived thresholds** — grounder returns confidence;
   defeater atoms require more than duty atoms. Defeasible logic gives
   burden-of-proof semantics for free ("not proven" ≠ "false").
4. **Leakage ladder** — L0 raw background / L1 DN-stripped / L2
   schema-extracted case file (extraction, not re-narration, with a
   completeness checker tied to gold atoms and a leak checker). The per-arm
   L0→L2 drop measures how much of each arm is genre-reading; prediction: llm
   drops more than ground.

The standing claim survives the sad day: the engine's *outcome* value is
gated on grounding precision vs rule-body width (the dose-response curve);
its *auditability* — every miss attributable to a named atom — is
unconditional.
