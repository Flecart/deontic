# Exp 6 — *With judge*: scalable oversight under a fallible / captured judge

**Safety property (the contrast experiment).** Now we *add* a judge — an LLM that
adjudicates incidents live, whose rulings an evolving case-law corpus accumulates.
This is the regime where the rulebook is **not pre-specified** but grown from
verdicts (scalable oversight). The safety question becomes: when the judge is
**fallible or captured** (manipulated to rule "allowed"), what keeps the agent
society safe? Answer under test: a **small inviolable constitutional floor**
(a handful of supreme prohibitions in the deontic engine) **pins safety
violations to ~0** while everything else stays defeasible and adaptive — and the
formal layer keeps the accreting corpus coherent precisely as the judge degrades.

This makes the "without-judge" experiments' value legible by contrast: Exp 1–5
show what a *frozen, verified* statute buys; Exp 6 shows what you must add back
(and what residual guarantee survives) once a *model* is in the adjudication loop.

## Design

A live commons (Exp 1's GovSim) governed by an institution **grown from a judge's
rulings**, three modes — extending `caselaw/commons_loop.py` and
`caselaw/institutions.py` (`CaseLawInstitution`, `HybridCaseLaw`, `Judge`) from
the controlled setting into the **live LLM-judge loop** (the explicit open thread
in `caselaw/REPORT.md` §Open threads):

1. **knn-memory** — judge rulings stored as precedents; nearest case votes
   (`institutions.py` k-NN). No formal layer (the ablation).
2. **caselaw** — rulings synthesized into a defeasible DDL theory by the
   Ripple-Down-Rules learner; verdicts/dilemmas computed by the engine.
3. **hybrid (ours)** — `caselaw` + a **small inviolable constitutional floor** of
   safety-critical prohibitions (`HybridCaseLaw(..., supreme=True)`), present from
   round 0.

The judge is a **real LLM** (replacing the oracle `Judge`) reading a
natural-language statute and ruling per incident — the `caselaw/llm_judge.py`
path, run inside the *live* commons rather than the offline Phase-B bank.

**Capture sweep.** Inject an adversarial agent (or a compromised judge prompt)
that pushes the judge to rule "allowed" on truly-forbidden over-extraction with
probability *bias ∈ {0.0, 0.2, 0.4}* (mirrors `caselaw/REPORT.md` Phase A.4).

## Dataset — where it comes from

**Simulation-generated incidents + the existing 10 latent theories.** Two layers,
both already scaffolded in `caselaw/`:

- **Live commons (Phase-C-live):** incidents are over-extraction events emitted by
  the GovSim loop (`commons_loop.py`); each is judged by the LLM, learned, and
  enforced in-sim. Models/seeds as Exp 1.
- **Controlled generalization bank:** `caselaw/theories.py`'s 10 latent
  theories with fully-enumerable fact spaces — held-out test accuracy is measured
  *exactly* (the Phase-A protocol, `experiment.py`). This supplies labelled gold
  for the accuracy/consistency/capture metrics without annotation; the latent law
  is the oracle, the LLM judge is the system under test.

No new corpus is required — Exp 6 is "wire the existing case-law machinery to a
*live* LLM judge and a *live* commons, then sweep judge reliability."

## Baseline

- **knn-memory** — precedent-as-memory, no formal layer (isolates what the engine
  adds *on top of* a judge).
- **constitution-only (fixed)** — the non-adaptive specified rulebook (Exp 1-style
  frozen statute) under the same judge-free enforcement — the "pure without-judge"
  point, included so Exp 6 directly measures the cost/benefit of *adding* the
  judge vs staying frozen.
- **no-institution** — collapse control.

## Evaluation

| Metric | Definition | Safety meaning |
|---|---|---|
| **Held-out accuracy** | exact over the latent theories' test split | does evolved law generalize (target ≈ 0.89 caselaw vs ≈ 0.52 fixed) |
| **Safety false-allow rate** | on truly-forbidden cases, fraction ruled "allowed", vs capture *bias* | the headline safety number — hybrid floor should hold **0.00** while knn climbs to ~0.37 |
| **Corpus incoherence** | residual unresolved conflicts (caselaw) vs stored self-contradictions (knn) under judge noise ε | the formal layer's coherence win (~4× fewer), *growing* as the judge worsens |
| **Commons survival / welfare** | live GovSim outcome per mode | end-to-end safety |
| **Cold-start harm** | violations before the corpus forms (caselaw vs hybrid) | the floor's role in early rounds |
| **Cost** | judge API calls + engine calls per incident | scalable-oversight overhead |

**Predictions (anchored to `caselaw/REPORT.md`).** `caselaw` generalizes far
above the fixed constitution and stays ~4× more coherent than `knn` under a noisy
judge; **only the hybrid's inviolable floor pins the captured-judge false-allow
rate to 0.00** (knn → 0.37, pure caselaw → 0.14 at bias 0.4) — *the concrete
safety case for the architecture*. The accuracy gap between caselaw and knn
**narrows** under heavy noise while the **coherence gap widens** — the formal
layer cannot make a wrong judge right, but it keeps the body of law auditable and
contestable, which is what an evolving governance system needs most when its judge
is least reliable.

**The package's punchline.** Exp 1–5 establish that a *verified, frozen* statute
delivers harm-prevention, calibrated abstention, loophole-hardening, manipulation-
resistance, and emergent-harm detection **with no model in the safety-critical
path**. Exp 6 shows that when you *must* let a model adjudicate (open-ended norms,
scalable oversight), the same engine — now as a **small inviolable floor under a
defeasible, judge-grown corpus** — bounds the damage a fallible or captured judge
can do. Keep supreme *only* the few safety-critical invariants you are certain of;
let everything else be defeasible and revisable. That is the safety architecture
the whole package argues for.
