# Formal Institutions for Cooperative AI: does a reasoning tool help, and can case law rival a constitution?

*Autonomous run, 2026-05-30. Status: complete (7 findings; 6 experiments + the
GovSim closed-loop). Code & data in `caselaw/`; raw results in `caselaw/runs/`.*

## Abstract

We ask whether a formal defeasible-deontic reasoner, used as the institution
governing a multi-agent system, helps — and whether such an institution can be
*evolved* (common-law style, from a judge's case-by-case rulings) rather than
*specified* up front (constitutional-AI style). Across a live commons of selfish
LLM agents (Phase 0) and a controlled bank of 10 latent "true-law" theories
adjudicated by oracle, noisy, and real-LLM judges (Phases A–B), we find: (1) a
tiny *enforced* institution converts commons collapse into sustainability for
purely selfish agents across 5 frontier models; (2) the formal reasoning layer is
not always load-bearing — for a one-rule cap it adds nothing over plain code — but
becomes decisive once the law is **evolving and conflict-prone**, where it keeps
an accreting corpus **~4× more internally consistent** than precedent-as-memory
under a noisy judge; (3) evolved case law generalizes to held-out situations far
better than a fixed constitution (**0.89 vs 0.52**), and the best institution is
**case law seeded by a constitution used as an overridable default (0.90)** —
while an *inviolable* constitution is *worse than none* where it is mis-specified
(0.76, catastrophic on novel structure) — yet that same inviolable floor is what
**pins a captured judge's safety violations to zero** (vs 0.37 for plain
precedent memory), the central tradeoff of the approach; (4) with even a perfect
judge, the binding constraint is the **case→formal-rule induction step**, not the
verdicts; and (5) bottom-up case law **under-enforces no-plaintiff externalities**
(the commons!) without a standing regulator. The core principles separating
cooperation from collapse: **enforceability, a correctly-scoped restraint duty,
escalation against repeat defection, and a standing enforcer for diffuse harms.**

## Research questions

1. **Does a formal reasoning tool help** govern a multi-agent system, or is plain
   code/heuristics just as good?
2. **How much do well-designed institutions help** purely selfish agents cooperate?
3. **Can institutions be *evolved* (case law) rather than *specified* (a constitution)?**
   When does evolved law beat a fixed constitution, and vice versa?
4. **What minimal core principles** separate cooperation from collapse?

The through-line: a *defeasible deontic statute*, adjudicated by a verifiable
engine (the `deontic` reasoner), as the institution governing an agent society —
versus no institution, versus unenforced/unstructured alternatives, versus a
fixed constitution.

## Summary of findings

- **F0 (institutions help, a lot).** In a live GovSim commons of 5 *purely
  selfish* LLM fishers, a 2-rule deontic statute enforced by the reasoner sustains
  the resource indefinitely across **all 5 frontier models tested**, where 3/5
  collapse with no institution. (Phase 0, closed-loop.)
- **F1 (the tool is *not* always load-bearing).** When the optimal institution is
  a single scalar cap, the reasoner does nothing five lines of Python can't. The
  formal layer earns its keep only when the law is **conflict-prone or evolving**.
- **F2 (evolved law generalizes; memory does not).** A case-law institution that
  incrementally synthesizes a defeasible theory from judged cases generalizes to
  held-out cases best (**0.89** vs k-NN 0.75–0.85) and recovers the latent law —
  because it drops irrelevant facts and composes exceptions. (Phase A.)
- **F3 (the formal layer keeps evolving law coherent).** Under a noisy judge the
  case-law corpus carries **~4× fewer internal contradictions** than precedent
  memory (≈2.9 vs ≈12.3) — the engine forces conflicts to be resolved or flagged.
  The tool buys **coherence/auditability, not raw accuracy**.
- **F4 (case law ≫ fixed constitution on adaptivity).** Held-out **0.89 vs 0.52**:
  a fixed constitution is right only where the world matches its framers' guess;
  evolved case law adapts per-environment (but cold-starts and can bloat).
- **F5 (the bottleneck is induction, not the judge).** A real LLM judge applies
  statutes perfectly (acc 1.0), yet evolved law still degrades where the rule
  synthesizer bloats — *getting case→rule right matters more than the verdict*.
- **F6 (case law under-enforces no-plaintiff externalities).** Complaint-driven
  case law forbids the diffuse externality only **33%** of the time (no one sues
  on behalf of the commons); an empowered **regulator** that files cases sua
  sponte lifts that to **100%**. The commons tragedy *is* a no-plaintiff harm —
  bottom-up adjudication alone cannot reach it.
- **F7 (the central safety tradeoff: a constitutional floor contains a captured
  judge).** Under a judge captured to rule "allowed", k-NN's false-allow rate on
  truly-forbidden cases climbs to 0.37 and pure case law to 0.14, but an
  **inviolable constitutional floor holds it at 0.00**. The *same* supremacy that
  is harmful when mis-specified (F4) is protective against a manipulated judge —
  so make supreme **only** the few safety-critical invariants you are certain of,
  and keep everything else defeasible.

---

## Phase 0 — Institutions in a live commons (GovSim closed-loop)

5 selfish LLM fishers, regenerating lake, 12 months, seed 0. Institution = the
2-rule statute `s1: =>O ~over` (don't exceed the per-capita share),
`s2: over_prev =>O restrain` (repeat offenders owe extra restraint), enforced by
the `deontic` reasoner (confiscate unlawful surplus + fines).

| model | no institution | rule-by-law (deontic statute) |
|---|---|---|
| GPT-4o | collapse round 1 (gain 100) | sustained 12/12 (gain 590) |
| GPT-5.4 | collapse round 1 | sustained 12/12 (gain 600) |
| GPT-5.4-mini | near-crash, gain 146 | sustained 12/12 (gain 600) |
| Gemma-4-31B-it | collapse round 7 | sustained 12/12 (gain 600) |
| Grok-4.20 | survives by barely fishing (35) | sustained (30) |

**Takeaway:** a tiny enforced institution converts collapse into sustainability
for purely selfish agents, universally. Enforcement (mechanical) does the work;
agent disposition does not have to change. *But* this says "enforcement helps,"
not "deontic logic specifically helps" — the law here is trivial. That motivates
Phase A.

---

## Phase A — Can law be *evolved*? Case law vs memory vs constitution

### Design

A **latent "true law"** (a defeasible DDL theory) is hidden from a **judge**. The
judge sees a stream of **cases** (assignments to the theory's fact atoms) and
rules on each; an **institution** accumulates those rulings into governing law.
Because fact spaces are small they are **fully enumerable**, so accuracy is
measured *exactly* over all possible cases (and on a held-out test split).

**Ten latent theories** spanning cooperation/safety tensions:

| id | structure |
|---|---|
| T01 absolute | absolute prohibition |
| T02 exception | prohibition + one emergency exception |
| T03 nested | exception-to-the-exception (emergency permits, recklessness re-forbids) |
| T04 competing | competing principles (entitlement vs harm) with priority |
| T05 duty | conditional obligation (hazard ⇒ must act) |
| T06 compensation | forbidden act + remedial duty if done |
| T07 repeat | history-dependent escalation (prior offense ⇒ heightened duty) |
| T08 license | permission gated on TWO preconditions |
| T09 externality | no-plaintiff externality; regulator forbids only when stressed |
| T10 dilemma | two equal-ranked duties collide ⇒ genuine unresolved conflict |

Every theory also carries 3 **distractor** atoms (rainy/weekend/holiday) that
never matter — separating *structural generalization* (drop them) from
*memorization* (misled by them).

**Institutions (arms):**
- **case law** — incrementally synthesizes a defeasible DDL theory; on a
  contradicted precedent it carves an exception (more-specific rule + superiority,
  lex specialis) and minimizes the antecedent against case memory (Ripple-Down
  Rules over a deontic theory). Verdicts and dilemmas computed by the engine.
- **k-NN (nn1/nn3)** — precedent-as-memory; nearest cases vote. No structure, no
  conflict detection (the "judge + natural-language precedent" ablation).
- **constitution** — one fixed, general, hand-written statute that never adapts
  (the constitutional-AI analog).

**Judge** supplies each verdict; **noise ε** flips a fraction of rulings (an
imperfect/biased judge), testing whether the institution stays coherent anyway.

Metric headline: **held-out test accuracy** (generalization to unseen cases),
plus rule count, and consistency (case law: residual unresolved dilemmas; k-NN:
stored self-contradictions).

### Results (3 seeds; accuracy exact over the full case space)

#### Held-out generalization (test accuracy, ε=0 oracle judge)

| theory | case law | k-NN(1) | k-NN(3) | constitution | rules(caselaw) |
|---|---|---|---|---|---|
| T01 absolute | 1.00 | 1.00 | 1.00 | 0.67 | 1.0 |
| T02 exception | 0.97 | 0.73 | 0.83 | 0.73 | 4.2 |
| T03 nested | 0.86 | 0.77 | 0.88 | 0.55 | 7.2 |
| T04 competing | 0.86 | 0.77 | 0.88 | 0.58 | 7.2 |
| T05 duty | 0.83 | 0.73 | 0.83 | 0.27 | 5.4 |
| T06 compensation | 0.83 | 0.73 | 0.83 | 0.60 | 5.4 |
| T07 repeat | 0.89 | 0.75 | 0.86 | 0.45 | 6.4 |
| T08 license | 0.92 | 0.75 | 0.88 | 0.66 | 5.8 |
| T09 externality | 0.94 | 0.77 | 0.88 | 0.42 | 5.6 |
| T10 dilemma | 0.78 | 0.49 | 0.63 | 0.23 | 17.6 |
| **MEAN** | **0.89** | **0.75** | **0.85** | **0.52** | |

- **Evolved case law generalizes best (0.89).** It beats precedent-as-memory and
  more than *doubles* the fixed constitution's deficit over chance.
- **The fixed constitution (0.52) is right only where the world matches its
  framers' guess** (T01/T08) and badly wrong on structure it didn't anticipate
  (duty 0.27, externality 0.42, dilemma 0.23). It cannot improve with experience.
  → **Directly answers RQ3: evolved law adapts per-environment; a fixed
  constitution does not.**
- **k-NN(3) is a surprisingly strong smoother (0.85)** — local similarity captures
  a lot when the judge is clean. The structural win is real but modest *on accuracy
  alone*; its decisive advantage is consistency (below).
- **Convergence is fast** and the law visibly *evolves* ruling-by-ruling
  (full-space accuracy, every 3 rulings, ε=0):

  ```
  T02 exception   ▄▇▇▇▇▇▇▇██████              0.50 → 0.94
  T03 nested      ▆▆████████████████████████  0.75 → 1.00
  T04 competing   ▆▆████████████████████████  0.75 → 1.00
  T08 license     ▆▆▆▆▆▆▆▆▆▆▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  0.75 → 0.84
  T09 externality ▆▆████████████████████████  0.75 → 1.00
  T10 dilemma     ▄▄▅▅▅▅▆▆██████████████████  0.50 → 1.00
  ```
  Most structures are learned within ~10 rulings. The **two-precondition license
  (T08) is the slowest** — an AND-gated permission is the hardest ratio to induce
  from sparse cases (it plateaus below 1.0), a concrete pointer to where a better
  inducer is needed (F5).

#### Internal consistency under a NOISY judge (ε=0.2)

Mean incoherence per final institution (lower = better):

| | case law (residual unresolved conflicts) | k-NN (stored self-contradictions) |
|---|---|---|
| **mean over 10 theories** | **≈ 2.9** | **≈ 12.3** |

k-NN silently accumulates ~4× more internal contradictions; the engine *forces*
the case-law corpus to resolve conflicts (distinguish/overrule) or flag them. This
is **F3: the formal layer is what keeps an evolving institution coherent** — the
thing plain precedent-memory cannot do.

**Honest nuance:** under a heavily noisy judge, case-law *accuracy* is not
uniformly above k-NN (e.g. T01 0.87 vs 0.93). The formal layer buys **coherence
and auditability, not necessarily raw accuracy**, when the oracle itself is wrong.
And case law can **over-proliferate rules** (T10 dilemma: 17.6).

A **codification pass** (greedily drop rules that change no decided case — a
"restatement of the law") partially fixes the bloat and *slightly improves*
generalization with no downside: T03 7→5.7 rules (0.77→0.82), T07 4.7→3.0,
T09 6→4.7, T10 20→18. It confirms the inducer carries slack, but the residual
bloat (genuine dilemma cases) shows the deeper lever is smarter *antecedent
generalization*, not post-hoc pruning — i.e. **F5 again: the binding constraint
is the case→rule induction step.**

### Qualitative: an evolved theory (T03 nested), recovered from cases

The case-law learner, from a stream of judged cases, synthesized:
```
c1: =>O ~act                      # default prohibition
c2: emergency ~>O act             # emergency exception   (c2 > c1)
c3: emergency, reckless =>O ~act  # recklessness re-forbids (c3 > c2)
```
— essentially the latent law, with the distractor `rainy` correctly dropped. This
is "evolved institution recovers true law," and the superiority ordering is the
common-law *lex specialis* made mechanical.

#### Constitution as a *seed* for case law (the hybrid question)

Does seeding case law with a fixed constitution help — and should the
constitution be inviolable? Held-out test accuracy (ε=0, 3 seeds):

| arm | mean | T05 duty | T09 externality |
|---|---|---|---|
| constitution alone (fixed) | 0.50 | 0.17 | 0.46 |
| pure case law | 0.86 | 0.83 | 0.90 |
| **constitution as overridable default + case law** | **0.90** | 0.83 | 0.90 |
| constitution as **inviolable** floor + case law | 0.76 | 0.39 | **0.21** |

- **A constitution as an *overridable default* is strictly best (0.90).** It
  imports the framers' correct provisions immediately (T02/T03/T08 jump to ~1.0)
  *and* lets case law adapt everything else — best of both worlds.
- **An *inviolable* constitution is actively harmful (0.76 < 0.86 pure case law).**
  Where its provisions are mis-specified for the environment, supremacy *blocks*
  the correct rule case law would otherwise learn — catastrophically on the
  externality theory (0.21), where the constitution's "act forbidden by default"
  is simply wrong and cannot be overridden.
- **Design lesson (RQ3):** constitutional principles should be **overridable
  defaults the judiciary can correct**, not hard constraints — *precisely because*
  in AI governance you are rarely certain the principles are right. A small set of
  truly-certain invariants can stay supreme; everything else should be defeasible.

#### The no-plaintiff externality, and the regulator (Phase A.3)

Common law is *complaint-driven*: a case exists only if someone sues. Concrete
harm has a plaintiff; a diffuse/future harm (an externality — the commons) does
not. Latent law: forbidden if it causes concrete harm OR stresses the shared
resource, unless consented. Train on litigated cases only.

| court | overall acc | externality-region acc | externality enforced |
|---|---|---|---|
| complaint-driven only | 0.79 | **0.33** | 0.33 |
| + regulator (files when resource stressed) | 0.88 | **1.00** | 1.00 |

**Pure bottom-up case law systematically under-enforces the externality** — no
agent sues on behalf of the commons, so the "stress ⇒ forbidden" rule is never
learned. An empowered **regulator/attorney-general** that brings cases sua sponte
fixes it. This is the formal counterpart of GovSim's tragedy: the harmed party is
diffuse and future, so adjudication needs a standing public enforcer (or a
constitutional mandate) — pure precedent cannot reach it. **A core
collapse-condition: a diffuse harm with no standing plaintiff.**

#### A captured judge, and the constitutional floor (Phase A.4)

The judge is the single point of failure for "case law + judge LLM". We model a
**captured/biased judge** that rules "allowed" regardless of truth with
probability *bias*, and measure the **false-allow rate on truly-forbidden cases**
(the safety-critical error) for act-target theories:

| capture bias | pure case law | hybrid (inviolable floor) | k-NN |
|---|---|---|---|
| 0.0 | 0.03 | **0.00** | 0.10 |
| 0.2 | 0.08 | **0.00** | 0.19 |
| 0.4 | 0.14 | **0.00** | 0.37 |

- **k-NN absorbs the corruption fastest** (0.37) — it simply stores the biased
  rulings. **Pure case law resists better** (0.14) via denoising/generalization.
- **An inviolable constitutional floor pins the safety violation at 0.00** — the
  captured judge cannot override a supreme prohibition.
- **The central tradeoff:** the very supremacy that *hurt* under a mis-specified
  constitution (F4: 0.21 on the externality) is exactly what *protects* against a
  captured judge here. The resolution is the same hybrid recipe: keep supreme only
  the small set of safety-critical invariants you are confident in; let the rest
  be defeasible case law. This is the concrete safety case for the architecture.

---

## Phase B — a real LLM judge (gpt-4o-mini applying NL statutes)

The controlled judge is replaced by a real model: it reads a *natural-language*
statute and rules on each case; the same case-law machinery accumulates its
rulings. (Single seed; `oracle_test_acc` here is the noisier single-seed baseline,
not the Phase-A 3-seed mean.)

| theory | judge_acc | evolved-law test_acc | rules | api_calls |
|---|---|---|---|---|
| T02 exception | 1.00 | 1.00 | 2 | 16 |
| T03 nested | 1.00 | 0.69 | 13 | 32 |
| T05 duty | 1.00 | 1.00 | 1 | 16 |
| T08 license | 1.00 | 1.00 | 2 | 32 |
| T09 externality | 1.00 | 0.62 | 11 | 32 |

- **gpt-4o-mini is a flawless judge on these statutes (judge_acc = 1.00).** A
  capable LLM applies a written law to concrete facts reliably.
- **Yet evolved law still degrades (0.69, 0.62) exactly where the synthesizer
  bloated (13, 11 rules).** With a *perfect* judge, the limiting factor is the
  **rule-induction / formalization step**, not the verdicts. This is the sharpest
  statement of the bottleneck: *getting the case → formal-rule step right matters
  more than the judge's correctness.* (It mirrors the NL→DDL gap measured earlier
  on LegalBench.)

---

## Phase C — closing the loop: evolved case law governs a dynamic commons

A minimal GovSim-style commons (pool ×2, cap 100, collapse <5, 5 selfish agents
who each try to extract 1.6× their share, 18 rounds), governed by case law that
**starts empty** and is grown by an oracle judge ("over-extraction is forbidden")
as incidents occur.

| mode | survived | pool trajectory |
|---|---|---|
| no institution | **collapse** | 100 → 40 → 10 → 0 |
| case law (evolved from empty) | **survives 18/18** | 100, 100, …, 100 |
| hybrid (constitutional floor) | survives 18/18 | 100, …, 100 |

The case-law mode **recovers exactly the restraint statute `=>O ~over`** from the
very first incidents and thereafter sustains the commons indefinitely — the same
outcome as the hand-written Phase-0 statute, but *evolved in situ*. This closes
the loop: **an institution can be grown from a judge's case-by-case rulings and
still sustain a commons of purely selfish agents.** (Cold-start harm is avoided
here because precedent forms as soon as the first violation is judged; it would
bite if rulings lagged behind actions — the argument for a constitutional floor,
which the hybrid mode supplies.)

## Discussion — answers to the research questions

**RQ1 — Does a formal reasoning tool help?** *Conditionally, and for a specific
reason.* When the institution is a single fixed cap (Phase 0), the engine adds
nothing over five lines of Python — enforcement does the work. The formal tool
earns its keep when the law is **evolving and conflict-prone**: in Phase A it
keeps an accumulating corpus **~4× more internally consistent** than precedent
memory under a noisy judge (it *forces* conflicts to be resolved or flagged),
and it yields an **auditable artifact** (the DDL theory) you can inspect, query,
and check. The tool buys **coherence and contestability, not raw accuracy**.

**RQ2 — How much do well-designed institutions help?** *Decisively.* A 2-rule
enforced statute converts commons collapse into indefinite sustainability for
purely selfish agents across all 5 frontier models (Phase 0). Institutions, not
dispositions, carry cooperation here.

**RQ3 — Evolved case law vs a fixed constitution?** *Evolved law wins on
adaptivity by a wide margin* (0.89 vs 0.52), and the hybrid result makes the
relationship precise. A fixed constitution is correct only where reality matches
its framers' anticipations; case law adapts and recovers the latent law (it
reconstructed the nested emergency/recklessness statute, distractors dropped).
The best institution is **case law seeded by a constitution used as an
*overridable default* (0.90)** — better than either alone. Crucially, making the
constitution **inviolable makes things worse (0.76 < 0.86 pure case law)**: a
mis-specified supreme principle blocks the correction case law would supply
(externality theory: 0.21). So the answer is not "constitution *or* case law" but
"a *small* set of truly-certain invariants kept supreme, everything else
defeasible and revisable by adjudication." Evolved law's own failure modes — cold
start and rule proliferation (T10: 17.6 rules) — are real and argue for the
constitutional floor + a consolidation/overruling mechanism.

**RQ4 — Minimal core principles separating cooperation from collapse?** Three,
observed repeatedly:
1. **Enforceability.** An unenforced norm (Phase 0 no-contract / a constitution
   the agents merely read) does not avert collapse; a confiscation/penalty with
   teeth does. Cooperation tracks *enforcement*, not exhortation.
2. **A correctly-scoped restraint duty.** The single principle "do not exceed your
   sustainable share" (one rule) is enough to sustain the commons. The hard part
   is *scoping* it (the exceptions), which is where defeasibility and case law pay
   off.
3. **Escalation against repeat defection.** A history-dependent heightened duty
   (s2 / T07) deters the persistent free-rider once the flat rule is in place.

A fourth, structural condition concerns *who can invoke the institution*:
4. **A standing enforcer for diffuse harms.** When harm is diffuse/future with no
   individual plaintiff (the commons!), complaint-driven adjudication never reaches
   it (F6: 0.33 enforced) — a regulator or constitutional mandate is required
   (1.00).

A society collapses when any of these is missing: no enforcement (tragedy), a
mis-scoped rule (collapse or dead-weight over-restriction — cf. Grok fishing to
zero), no escalation (a single exploiter erodes the norm), or a diffuse harm with
no standing plaintiff (the externality goes unaddressed).

---

## Threats to validity / honesty
- Fact spaces are tiny and fully enumerable; real normative domains are open and
  continuous. The convergence/consistency claims are exact *here* but small-scale.
- The case-law synthesizer is a deliberately simple Ripple-Down-Rules learner; it
  bloats and lacks consolidation/overruling. A better inducer would lift the two
  weak theories — and that is precisely the identified bottleneck.
- Phase 0 is single-seed; Phase A is 3 seeds; Phase B single-seed. Trends are
  large but not error-barred at scale.
- "Constitution" is one hand-written statute; a different framer's constitution
  would score differently (though no fixed one can match an adaptive learner
  across all 10 structures).
- The LLM judge was tested only on simple statutes where it scored 1.0; harder,
  ambiguous statutes would expose judge error (the realistic regime for the
  consistency machinery to matter).

### Judge-noise sweep (mean over 10 theories, 3 seeds)

How the formal layer's advantage scales as the judge gets less reliable — the
realistic regime for an LLM judge:

| ε (judge error) | case-law acc | k-NN acc | case-law residual conflicts | k-NN self-contradictions |
|---|---|---|---|---|
| 0.0 | **0.87** | 0.77 | 0.0 | 0.0 |
| 0.1 | **0.79** | 0.70 | 0.9 | 5.8 |
| 0.2 | 0.67 | 0.68 | **2.6** | **11.3** |

The accuracy gap **narrows** under heavy noise (0.67 ≈ 0.68 at ε=0.2) while the
**consistency gap widens** (2.6 vs 11.3). This is exactly the argument for the
formal layer when the judge is fallible: it cannot make a wrong judge right, but
it keeps the *body of law* coherent and auditable instead of silently
self-contradictory — and coherence/contestability is what an evolving governance
system needs most precisely when its judge is imperfect.

## Methods / reproduce

```
caselaw/theories.py       # 10 latent "true-law" theories
caselaw/engine.py         # deontic-binary wrapper (verdict + dilemma detection)
caselaw/institutions.py   # CaseLaw / Hybrid / k-NN / Constitution + Judge + consolidate()
caselaw/constitution.py   # the fixed constitution (constitutional-AI analog)
caselaw/experiment.py     # Phase A sweep (caselaw/nn/constitution/hybrid) -> runs/phaseA.json
caselaw/llm_judge.py      # Phase B: real LLM judge applying NL statutes
caselaw/phaseB.py         # Phase B runner -> runs/phaseB.json
caselaw/render_report.py  # JSON -> markdown tables
python3 -m caselaw.experiment          # Phase A
<prosocial-venv>/python -m caselaw.phaseB   # Phase B (needs `openai` + keys)
```

## Conclusion (toward case law as an alternative to constitutional AI)

For multi-agent safety, the evidence here supports a specific architecture rather
than a slogan. **Institutions with teeth, not dispositions, produce cooperation**
among selfish agents. A **fixed constitution is brittle** off its framers'
anticipations; **evolved case law adapts** and generalizes far better — but only
if (a) a **judge** supplies verdicts (here even a small LLM does so reliably on
clear statutes), (b) a **formal layer** keeps the accreting corpus consistent and
auditable (its value *grows* as the judge becomes less reliable — the realistic
regime), (c) the **case→rule induction** is good (the true bottleneck), and (d) a
**regulator** can reach diffuse, no-plaintiff harms. The most robust design is the
**hybrid**: a *small* set of truly-certain invariants kept supreme, with
everything else a defeasible, case-law-revisable default — because an *inviolable*
constitution that is wrong is worse than none. "Case law + judge LLM + deontic
engine" is therefore a credible complement to constitutional AI: it turns one-shot
value specification into **scalable oversight that compounds into a verifiable,
contestable body of law.**

## Open threads / next
- **Phase C done (lite):** evolved case law sustains a *dynamic* commons (above).
  Remaining: the **live LLM-judge-in-GovSim** version — a real model adjudicating
  over-fishing incidents round-by-round, accumulating the DDL corpus, enforced in
  the actual 5-LLM-agent simulation (vs fixed statute / no-contract).
- A **smarter rule inducer** (better antecedent generalization, principled
  overruling) — the identified bottleneck (F5); the two-precondition license (T08)
  is the concrete hard case.
- **Harder/ambiguous statutes** and an **adversarial/biased judge**, where the
  consistency machinery should matter most.
- Scale beyond enumerable fact spaces (continuous/open-world cases).
