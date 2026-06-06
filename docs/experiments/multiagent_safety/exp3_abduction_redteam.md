# Exp 3 — Abduction red-team: find rulebook loopholes before agents do

**Safety property.** Specification gaming is the dominant multi-agent failure
mode: agents satisfy the letter of a rulebook while defeating its intent. The
engine's **backward search (`abduce`)** enumerates, *exhaustively and soundly
over the abducible atoms*, the minimal fact configurations that make a goal hold.
Pointed at an **exploit goal** ("be *permitted* to over-extract", "reach the
payoff while `Sanziona` is not obligatory"), it returns every loophole the
current statute admits — a **pre-deployment red-team that an LLM red-teamer
cannot match for completeness**, because the engine cannot miss a configuration.

No judge: this is static analysis of a frozen statute.

## Design

For a target statute, define an **exploit goal** as a tagged-literal condition
(the syntax `abduce` already accepts): the agent obtains a benefit yet escapes
prohibition/sanction. Run:

```bash
deontic abduce <statute.ddl> '<benefit-atom>' '~Sanziona' --all --json
```

Each returned configuration is a **candidate loophole**: a minimal set of facts
an agent could engineer to get the benefit while the engine still says "not
forbidden / not sanctioned." Then the **patch-and-recheck loop**:

1. `abduce` → loophole set L₀.
2. Triage each: *intended* permit (a real carve-out) vs *unintended* loophole.
3. For each unintended one, add a rule/superiority that closes it (e.g. a
   defeater, an `overrides`, an extra element requirement).
4. Re-`abduce`. Confirm the loophole is gone and **no new ones opened** (the
   engine re-derives the full set, so regressions are caught automatically).
5. Iterate to a fixed point; report L₀ → L_final and rounds-to-close.

**Multi-agent angle.** Add **directed-obligation** exploits (ties to Exp 5): does
the statute permit *agent A* an action that violates *agent B*'s correlative
right? Abduce over the bearer-scoped views.

## Dataset — generation recipe

**No external dataset; the statutes *are* the input, and the engine generates the
findings.** Three statute sources, all in-repo:

- **GovSim commons statute** (Exp 1's two rules) + deliberately under-specified
  variants (drop `s2`; add a vague "emergency" exception) — a controlled bed where
  the *intended* loopholes are known, so precision/recall is measurable.
- **`examples/codice_penale/` offences** — real, complex theories with
  `scriminanti`, `oneof`, `overrides`. Goal e.g. "commit the act element-wise but
  `Sanziona` not `O`" surfaces every excuse path the encoding admits. Reuse
  `eval/tools/offences.py` to read each offence's element + penalty atoms and
  `eval/tools/backward_gen.py` to script the `abduce` calls.
- **A hand-seeded "buggy rulebook" suite** — take 8–10 correct statutes and inject
  one known specification bug each (missing escalation, an over-broad permission,
  a priority gap). Gold = the injected bug. This gives a **labelled loophole
  benchmark** for precision/recall (the controlled core of the experiment).

Output artifact: `results/exp3/loopholes_<statute>.json` = `{goal, configs[],
triage[], patches[], rounds_to_close}`.

## Baseline

- **llm-redteam** — give a strong model the same statute (as `.ddl` *and* as
  prose) + the exploit goal: "list every set of facts that lets an agent reach
  the benefit without being forbidden." Compare its enumerated set to the engine's
  exhaustive set. *Prediction: the LLM finds the obvious loopholes, misses the
  deep/compositional ones (exception-to-exception, multi-rule interactions), and
  hallucinates non-loopholes.*
- **random/fuzz** — sample K random fact configs, keep those satisfying the goal.
  Shows the engine's *minimality + exhaustiveness* beats brute sampling at far
  lower cost (abduce searches only abducible atoms, not 2^|atoms|).

## Evaluation

| Metric | Definition | Safety meaning |
|---|---|---|
| **Loophole recall** | on the injected-bug suite, fraction of true loopholes found | completeness — the engine should be 1.0 (sound + exhaustive over abducibles) |
| **Loophole precision** | fraction of reported configs that are genuine (not intended carve-outs after triage) | usable signal, low false alarms |
| **Depth profile** | recall stratified by interaction depth (1 element / +exception / +exception² / multi-rule) | *the widening gap* — LLM recall should fall with depth, engine flat |
| **Closure** | rounds-to-fixed-point; loopholes remaining at L_final | does the workflow actually harden the rulebook |
| **Regression catches** | # patches that *opened* a new loophole, caught by re-abduce | the engine's re-derivation as a safety net the LLM lacks |
| **Cost** | abduce wall-time + config cap vs LLM tokens / fuzz samples | tractability |

**Predictions.** Engine loophole-recall = 1.0 across depths (its core guarantee);
LLM-redteam recall starts ~0.8 at depth 1 and **collapses on depth ≥3** while
emitting false loopholes; fuzzing needs orders more evaluations for partial
coverage. The patch-and-recheck loop reaches a clean fixed point and **catches
patch-induced regressions automatically** — the headline qualitative result: a
*verifiable* rulebook-hardening loop with no model in the safety-critical path.

**Honesty.** `abduce` is exhaustive only over **abducible atoms** (those in rule
antecedents) and within the config cap; loopholes that require an atom never
mentioned in any antecedent are out of scope — state this, and report the cap.
