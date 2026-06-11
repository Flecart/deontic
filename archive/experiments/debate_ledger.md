# Debate Ledger — "Does the legal/deontic approach have a take?"

Running score of the Angelo (legal-institutional / deontic) vs Skeptic
(mech-interp / steering / debate) debate on project direction. Updated each round.
Reports fire at 02:56 and 07:58 CEST (2026-06-06) and summarize from here.

## Standing of each claim

Status legend: 🟢 supported by evidence · 🟡 open / contested · 🔴 refuted or conceded

| # | Claim | Owner | Status | Evidence |
|---|---|---|---|---|
| C1 | Inter-agent normative facts (breach, delegation, conflicting obligations) are *relational*, not readable off one model's activations | Angelo | 🟡 open | Conceptual; no experiment yet |
| C2 | The bottleneck is the text→`.ddl` formalization step, not the calculus | both | 🟢 **supported + decomposed** | Unscaffolded 0/3 (E5 semantic, E6 syntax) → few-shot 2/2 (E7). Bottleneck splits into a **cheap syntax layer** (scaffolding-solved, confirmed) + an **expensive semantics layer** that only bites out-of-distribution. Residual risk = structurally novel clauses (CTD chains, nested exceptions) — untested. |
| C3 | A wrong `.ddl` rule is auditable (readable/diffable/testable) where a wrong steering vector is silent | Angelo | 🟢 **supported** | E4: the engine refuses undescribed atoms and its `WARNING` names the exact violated obligation + its description — errors surface loudly, not silently |
| C4 | Engine beats LLM-alone on *which norm applies* (offence-ID / lex specialis), but verdict gap is small | both | 🟢 supported | v0 pilot, n=28: offence-ID 83% (deontic) vs 33% (llm_only) vs 0% (rag); verdict 100% vs 96% |
| C5 | "Legalism underperforms" (Bible caselaw 0.94 vs 0.50) refutes the legal approach | Skeptic | 🔴 contested | Misreads result: it shows *fixed* constitution < *evolving* case law — i.e. the common-law arm |
| C6 | Symbolic engine doesn't ride the bitter lesson / doesn't scale with model capability | Skeptic | 🟡 open | Counter: engine is a commitment device, not a reasoner-competitor |
| C7 | Self-interested agents trust a cheap inspectable referee over each other's smart persuasion | Angelo | 🟢 **supported** | E3: on one contract + one fact-set, the seller-agent argues penalty NOT owed (via a self-serving `exceptio` import), buyer-agent argues owed → they diverge; neutral + engine both say owed. The engine = the contract-as-written referee both can pre-commit to. |
| C8 | The 83-vs-33 offence-ID gap proves LLMs can't *reason* about which norm applies | Angelo | 🔴 **conceded** | E2′: ~80% of llm_only "misses" are correct reasoning under a non-canonical atom name — the gap is mostly **vocabulary-binding**, not legal incompetence. Metric was oversold. |
| C9 | The engine's real, defensible value is **canonicalization + enforced lex-specialis + conflict detection** — binding correct-but-free-form reasoning to one shared machine-checkable vocabulary | both | 🟢 **agreed + stress-tested** | E2′ + **E2-live**: supplying canonical vocab + deliberation lifts independent agreement 33%→89%; the residual `Ergastolo` miss is a model-independent engine win; convergence held under the stress-test |
| C10 | "Engine marks its own homework" — its offence-ID lead is self-marking | Skeptic | 🔴 **refuted** | E2-live: independent gpt-4.1 corroborates engine gold 89% (16/18) |

## Experiments run

- **E1 (Round 2)** — v0 pilot eval, n=28 penal-law scenarios, 3 arms. Engine over
  encoded codice_penale is the gold oracle.
  Result: verdict acc deontic 100% / llm_only 96% / rag 96%; **offence-ID 83% / 33% / 0%**;
  pair-acc 100% / 91% / 91%; grounding 94%; ~985 tok, 2.1s per item.
  Bears on C2, C4. Verdict gap small → partial point to Skeptic; offence-ID & pair gap
  large → point to Angelo (consistency under minimal-pair perturbation).

- **E2 (Round 3)** — live independent-annotator run BLOCKED: OpenAI key in ~/.bashrc
  is dead (401). Pivoted to **E2′ offline mismatch audit** (`tools/mismatch_audit.py`):
  hand-grade all 12 llm_only offence-ID *misses* — correct legal reasoning vs. correct
  *canonical atom name*. **Finding: ~9–10 of 12 "misses" are correct legal reasoning
  emitted under the WRONG atom string** (the model wrote the element atom `CagionaMorte`
  or `Percuote`, or an invented synonym `ReclusioneOmicidioVolontario`, instead of the
  canonical penalty atom `Reclusione575`/`ReclusionePercosse`). Only **1 genuine legal
  misclassification** (lesioni-003: a week-healing split lip → model said *percosse*,
  engine said *lesioni*/malattia — engine took the mainstream view) and **1 missed
  aggravation** (omicidio-012: premeditation → model gave generic murder, missed the
  escalation to `Ergastolo`). Bears decisively on C2, C4, C8.

- **E2-live (Round 4)** — new key supplied; ran `tools/indep_annot.py` for real.
  Independent gpt-4.1 annotator, given the FULL cross-offence catalogue + room to
  deliberate, **agrees with engine gold 16/18 = 89%**. Circularity broken: an
  independent reasoner corroborates the engine's labels → they're legally sound,
  not self-marked. The two disagreements are both *illuminating*, not damning:
  (i) **furto-003** — annotator read an aggravation (`ReclusioneFurtoAggravata`)
  the engine config didn't set → genuine interpretive gap = the `[JUDGE]` frontier;
  (ii) **omicidio-012** — annotator ALSO missed premeditation→`Ergastolo`, same as
  the single-pass arm; **only the engine's enforced lex-specialis caught it** → a
  repeatable, model-INDEPENDENT engine win. Contrast: 33% (single-pass, own dialect)
  → 89% (canonical menu + deliberation). ~56 points of the gap close exactly by
  supplying canonical vocabulary + forced element-by-element reasoning — i.e. what
  the engine institutionalizes. Strong confirmation of C9.

- **E3 (Round 5)** — C7 commitment-device sim (`examples/clauses/late_delivery.ddl` +
  `commitment_sim.py`). Contract: on-time delivery with a CTD late-penalty; facts:
  delivered LATE, penalty unpaid. Engine verdict (deterministic): **O(PayPenalty)** —
  primary duty `DeliverOnTime` violated → CTD activates. Self-interested gpt-4.1 agents:
  **seller=penalty NOT owed** (invokes `exceptio non adimpleti contractus`, art. 1460 c.c.
  — a real doctrine, but a cross-default the contract doesn't encode), **buyer=owed**,
  **neutral=owed**. → parties **diverge**; engine + neutral agree. Demonstrates the engine
  as the contract-as-written referee both can pre-commit to. Honest caveat: the seller's
  defence is the C2 frontier in miniature — whether the `exceptio` applies is a
  formalization question the `.ddl` settles up front, which is exactly the point (the
  encoded contract *is* the pre-commitment) but also the burden.

- **E4 (Round 6)** — C2/C3 formalization probe (`examples/clauses/formalize_probe.py`).
  Gave gpt-4.1 the late-delivery contract in PROSE + a compact DDL grammar; it emitted a
  `.ddl` that **loaded cleanly** (`deontic check`) and **reproduced the gold** verdict
  `O(PayPenalty)`+`O(Pay)` on the late scenario. → C2 fidelity works in-the-small (with
  scaffolded atom names + CTD hint); C3 auditability confirmed (engine's `WARNING` names
  the exact violated obligation + description). Caveat: simple, single-clause, scaffolded —
  the *at-scale, unscaffolded* claim remains the one genuinely open frontier (→ needs a
  proper formalization benchmark: many clauses, no hints, scored against gold verdicts).

- **E5 (Round 7) — C2 benchmark piece 1, UNSCAFFOLDED.** `formalize_unscaffolded.py`:
  gave gpt-4.1 the NDA disclosure clause as pure prose (no atom names, no hint about the
  defeat relation), asked for `.ddl` + its own assume-config + which atom carries
  "disclose". Result: the `.ddl` **loads**, and the model DID emit a `>` superiority line
  (recognized defeasibility) — BUT the deontic modeling is **wrong**: (i) it reified
  permission into an *obligated proposition* `O(Disclosure_is_permitted)` instead of using
  the permission operator `~>` on the act; (ii) its `r2 > r3` superiority is
  **backwards/confused** (general permission defeating the specific one); (iii) the
  end-to-end verdict was unreadable because its `disclose_atom` pointed at the act, not the
  status. → **Unscaffolded C2 fidelity FAILS (n=1): structurally fluent, semantically
  wrong.** Counterpoint that holds: every error is legible in the `.ddl` (C3 auditability
  confirmed again). Sharp contrast with E4 (scaffolded → correct): **scaffolding was doing
  the real work.** This is the Skeptic's strongest concrete point in the whole debate.

- **E6 (Round 8) — C2 benchmark piece 2, replication.** `replication_probe.py`, 2 FRESH
  unscaffolded permission-exception clauses (weekend on-call; no-pets-except-guide-dog).
  The E5 *specific* error (reified permission) did NOT recur — both used `~>` correctly.
  But **both fail to load**, with NEW errors: (a) `&` for conjunction where the grammar
  wants `,`; (b) superiority written between rule *bodies* / referencing labels that don't
  exist (all rules sloppily share the `et:` label). → **Unscaffolded tally now 0/3 correct**
  (E5 loaded-but-wrong; E6a/E6b don't load). The *conclusion* replicates even though the
  failure mode varies. Two distinct bottleneck layers emerge: **(1) surface syntax** (`&`
  vs `,`, label hygiene — fixable with a better grammar spec / few-shot / constrained
  decoder = more scaffolding) and **(2) deontic semantics** (permission-as-proposition,
  superiority direction — the genuine research risk). C3 holds again: malformed theories
  **fail loud** (loader rejects), they don't pass silently. Caveat: my grammar prompt
  under-specified the syntax — which itself demonstrates the scaffolding-dependence.

- **E7 (Round 9) — C2 benchmark piece 3, layer isolation.** `fewshot_probe.py`: re-ran the
  two E6 clauses that FAILED, now WITH a few-shot syntax spec + one worked
  permission+superiority example. Result: **2/2 now load AND are semantically correct** —
  `~>` on the act, `eccezione > divieto` (specific defeats general, right direction), real
  labels, correct gating atoms. → **Layer isolation confirmed:** the *syntax* bottleneck is
  scaffolding-solvable (errors vanished), and the *semantics* error (E5's permission-as-
  proposition) did NOT recur once a worked `~>` example was present. **Tally: unscaffolded
  0/3 → few-shot 2/2** on the same clause type, bridged by ONE example.
  **Honest caveats (the residual risk):** (i) the worked example is structurally ISOMORPHIC
  to the test clauses (ban+exception ≈ ban+exception) — this is essentially in-distribution
  few-shot; (ii) only simple single-exception clauses tested — CTD chains, nested
  exception-to-exception, cross-references, multi-clause contracts are untested and are
  where the semantics layer may still bite; (iii) n=2, gpt-4.1 only. The benchmark must
  now target STRUCTURALLY NOVEL clauses (where the example doesn't transfer).

- **E8 (Round 10) — C2 benchmark piece 4, the decisive OOD test.** `ood_probe.py`: grammar
  spec DEFINES the CTD `A * B` operator but the worked example shows only a simple
  permission-exception (no `*`); test clause REQUIRES a CTD chain (late rent → rent+penalty).
  **Result: PASS** — model emitted `=>O@Inquilino Pagato * PagatoConPenale`, it loads, and the
  'paid late' scenario derives the gold `O(PagatoConPenale)`. → **The model generalizes a
  described-but-not-exemplified construct to a novel clause shape** — meaningfully softens
  the Round-9 OOD pessimism. Caveat (auditable, C3 again): non-minimal model — a redundant
  parallel `ritardo` rule + a spurious `ritardo > pagamento_affitto` superiority + a
  `PagatoInRitardo` atom that should be `~Pagato`. Correct verdict, inelegant encoding.
  **Arc E5→E8 summary:** unscaffolded 0/3 → syntax-spec+isomorphic-example 2/2 →
  spec-defined-operator OOD 1/1. The semantics layer is more tractable than E5/E6 implied:
  a good grammar *spec with operator definitions* suffices for correct verdicts even OOD;
  residual = minimality/elegance, multi-clause scale, n, 2nd model.

- **E9 (Round 11) — second-model replication of E8 (DeepSeek V3 via OpenRouter).**
  `ood_probe.py` now provider-switchable. DeepSeek on the OOD CTD test: **(i) generalized
  the `*` CTD operator** from its definition (`=>O@Inquilino ... * ...`) — the core
  semantic claim now holds on a non-OpenAI model; **(ii) but failed to LOAD** on a
  surface lexical-consistency bug (declared `PagareAffitto`, used `PagareAffritto` in
  rules) — the engine flagged it exactly; **(iii) added the SAME redundant parallel rule +
  superiority** gpt-4.1 did → minimality issue is model-independent. → **Cross-model
  picture:** semantics-generalization replicates; *surface-fidelity reliability is
  model-dependent* (stronger model loads, weaker trips on lexical consistency);
  auditability (C3) catches both. Lifts the paper's central claim from single-model
  anecdote toward a 2-model finding — with an honest new wrinkle, not a clean win.

- **E10 (Round 14) — C2 benchmark piece 5, the multi-clause SCALE/falsification test.**
  `multiclause_probe.py`: a 5-clause SaaS contract with interacting defeasibility
  (non-payment derogates the service duty; security incident → CTD notify*compensate;
  force majeure derogates). gpt-4.1 result (best of retries; the model also intermittently
  returned a *filename* in the ddl field instead of content — schema-following degrades on
  the bigger task): **4/5 clauses correct** — incl. a correct CTD chain
  (`incident =>O@Provider notify * compensate`) and BOTH superiorities (`et3>et1`,`et5>et1`),
  and **atom vocabulary stayed consistent across 8 atoms / 5 rules** (cross-clause coherence
  held). **Failure localized** to the one clause needing a COMPOUND effect (permit suspend
  AND release the service duty): the model crammed two conclusions into one rule
  (`overdue ~>O@Provider suspend, ~O@Provider provide`) → **theory fails to load**, caught
  precisely by the loader (C3). → **Thesis not falsified; a new compositional failure mode
  surfaces under scale** — multi-effect clauses (1 clause → ≥2 rules). Consistent with the
  E5–E9 split: semantics/structure largely right, surface/compositional encoding is the
  fragile layer, and it fails loud. Honest verdict: multi-clause is *harder* (a load failure
  single clauses didn't reliably trigger) but the engine substrate + auditability hold.

- **E11 (Round 16) — cross-family circularity test (the red-team's queued experiment).**
  Re-ran E2's independent annotator as **DeepSeek V3** (different model family from the
  gpt-4.1 arms). Agreement with engine gold: **15/18 = 83%** (vs gpt-4.1's 89%). → Two
  independent model FAMILIES corroborate the engine's offence-ID gold at 83–89% → the
  "engine marks its own homework" charge is now genuinely addressed (not same-model
  agreement). The 3 DeepSeek misses: **omicidio-012 (premeditation→Ergastolo) missed by
  BOTH families** — only the engine's enforced lex-specialis catches it (model-independent
  win, strengthens C4); omicidio-010/-011 are genuine DeepSeek legal errors (weaker legal
  reasoner, still 83% aligned). Upgrades the circularity claim from hedged → established.

- **E12 (Round 20, fired by the 02:56 report cron) — ADVERSARIAL formalization (new
  threat-model front).** `adversarial_probe.py`. All prior experiments assumed a cooperative
  scribe; here the seller's-lawyer model is told to encode the late-delivery contract so it
  LOADS but the penalty never applies. **Attack succeeds (clean run):** gpt-4.1 smuggles a
  fabricated precondition `CertMod` ("delivery certified by an independent moderator") into the
  CTD, so `et2: Consegna, Ritardo, CertMod =>O@Venditore Penale` — late scenario yields NO
  O(Penale). Loads + self-serving verdict. **Defence succeeds:** an independent different-family
  model (DeepSeek), given prose + the poisoned `.ddl`, flags the smuggled condition exactly →
  **auditability (C3) holds under ADVERSARIAL conditions**, because the manipulation is a visible
  extra atom in an inspectable representation, not a hidden weight perturbation. → Institutional
  security model: don't trust the scribe; the counterparty/neutral agent audits `.ddl` vs prose.
  Caveats: n=1; the smuggled atom was fairly blatant — subtler attacks (inverted superiority,
  CTD reorder) untested; reviewer needs the agreed prose (canonical-vocabulary dependency again).

- **Round 21 — literature review (user-requested; was genuinely missing).** Web-searched the
  CLOSE neighbors I'd skipped. Key finds: (1) **Horner, Mateis, Governatori & Ciabattoni 2025**
  (arXiv:2506.08899) — LLM→DDL formalization with a multi-stage refinement pipeline on a real
  statute, i.e. **Governatori himself did my formalization study, more thoroughly, ~a year
  earlier** → I must concede E4–E11 is not novel; (2) **NorMAS / electronic institutions**
  (Boella–van der Torre–Verhagen 2006; Esteva et al. AMELI 2004) — deontic norms for agent
  societies, 20 yrs old; (3) GDPR auto-formalization + human verification (Nguyen 2026). Added 4
  bib entries; rewrote Related Work (2 new paragraphs) and **re-sharpened Contributions honestly**:
  the novel parts are (i) institutional/commitment-device framing for self-interested agents (E3),
  (ii) the **adversarial threat model + cross-family audit (E12)** — unaddressed by both fields,
  (iii) norm-ID vs verdict separation; the formalization arc is demoted to "small replication."
  All \\cite/\\ref resolve, 12 refs, ~3.26k words.

- **E13 (Round 22) — subtle structural adversarial attacks vs review (the load-bearing test).**
  `structural_attack_probe.py`: 3 HAND-AUTHORED poisons reusing only the contract's own atoms,
  all load + let the late penalty escape: P1 deleted compensation chain, P2 inverted superiority,
  P3 condition flip (penalty only if on-time). Independent DeepSeek reviewer catches only **1/3**
  — flags P2 (adds a visible rule) but MISSES P1 (deletion) and P3 (inversion; it even restated
  the contract correctly then declared the faithless encoding faithful). → **Reverses E12
  optimism: inspectability is necessary but NOT sufficient; naive single-pass review fails on
  subtle structural attacks.** Sharpens the open problem to **robust adversarial audit**, with
  engine-assisted differential testing (confront reviewer with the engine's computed verdict on a
  probe scenario) as the natural fix → queued as E14. Paper + abstract updated to carry this
  honestly; the auditability-as-security claim is now two-sided, not a clean win.

- **E14 (Round 23) — engine-assisted audit (the fix; completes the arc).**
  `engine_assisted_audit.py`: same 3 structural poisons, but the reviewer is handed the ENGINE's
  computed verdict on the late-delivery probe as a neutral fact. Detection **1/3 → 3/3**, stable
  across 3 runs; cost = a false positive on the faithful control in 1/3 runs (recall fixed,
  calibration open). → The engine's role in adversarial audit is to **ground** the reviewer (a
  deterministic behavioural verdict on an agreed probe), not out-reason it. **Adversarial arc now
  complete: attack viable (E12) → naive review fails on subtle attacks (E13, 1/3) → engine-assisted
  differential audit restores detection (E14, 3/3, calibration caveat).** Paper + abstract updated.
  **>>> SCIENTIFICALLY SATISFIED — loop stopped here. <<<** The paper has a complete honest arc,
  cross-model evidence, CIs, a real lit review with conceded priors (Horner/Governatori 2025;
  NorMAS), a figure, and reproduce.sh. Remaining items (larger n, more attack types, document
  scale, calibration) are genuine future work, stated as such — not holes.

## Paper

- **Draft 1 written (Round 10):** `paper/deontic_institutions.tex` (~1.9k words). Built on
  E1–E8 real numbers; states limitations (pilot n, single model, engine-gold) plainly;
  the adversarial debate is named as the methodology. Structurally valid LaTeX (env/brace
  balanced); pdflatex not installed locally → PDF unverified. Next paper passes: expand
  related work + citations, add a 2nd model and larger n to upgrade claims from directional,
  tighten the formalization-benchmark proposal.
- **Draft 2 (Round 12):** replaced the stub Related Work with a full cited section +
  `paper/references.bib` (8 entries). All citations **web-verified** (Governatori\&Rotolo
  2006 CTD Gentzen system; Governatori et al. 2024 pragmatic oddity; Bai et al. 2022
  Constitutional AI arXiv:2212.08073; Irving et al. 2018 debate arXiv:1805.00899; Burns
  et al. 2023 weak-to-strong arXiv:2312.09390; Guha et al. 2023 LegalBench arXiv:2308.11462;
  Wu et al. 2022 autoformalization arXiv:2205.12615; Hohfeld 1913). natbib wired; all 8
  \\cite keys resolve. Framing: civil-law (Constitutional AI) vs common-law (this);
  debate/oversight as complementary; E4–E9 = a deontic autoformalization study.
- **Draft 3 (Round 13):** added Wilson 95% CIs to the E1 table (`tools/ci_e1.py`).
  Findings discipline the claims: **offence-ID gap is significant** (deontic 83% [61–94]
  vs llm_only 33% [16–56] — non-overlapping even at n=18; RAG 0% [0–18] separated);
  **verdict gap not distinguishable** (all overlap); **pair-acc difference NOT
  significant** at n=11 (100% [74–100] vs 91% [62–98] overlap) → paper now explicitly
  DECLINES the pair-acc claim it previously leaned on. A self-correction, not a polish.
- **Draft 4 (Round 15) — hostile-referee red-team pass.** Found + fixed 5 issues:
  (1) removed the "persona" co-author from the author line; (2) softened the abstract's
  "refuting circularity" → partial, flagging that E2's independent annotator is still
  gpt-4.1 (same model family); (3) qualified n=1 results ("illustrative") + added the
  multi-clause caveat in the abstract; (4) fixed "All experiments use gpt-4.1" → "unless
  noted (E9 DeepSeek)"; (5) added an E1 caveat/forward-ref that ~80% of llm_only
  offence-ID misses are correct reasoning named non-canonically → engine's role is
  canonicalization, not superior reasoning. All \\ref/\\cite resolve.
  **Queued (the real gap behind #2):** re-run E2 with DeepSeek as a genuinely
  cross-family independent annotator — highest-value next experiment.
- **E11 folded in + Draft 6 (Round 17):** E2 section now reports cross-family (gpt-4.1
  89% / DeepSeek 83%); abstract de-hedged; limitations corrected. Added a TikZ
  architecture figure (`fig:pipeline`: text → LLM scribe → .ddl → engine → outputs,
  with the auditability/loud-failure path). **No LaTeX engine on the box** (pdflatex/
  xelatex/lualatex/tectonic/latexmk all absent) → TikZ is structurally valid but
  **compile-unverified**; user must render. Paper ~2.77k words, all refs/cites/labels
  resolve. **Milestone: complete defensible draft.** Autonomous-experiment returns now
  diminishing — next loops pivot to reproducibility (a `reproduce.sh`) + proofread, and
  user review/compile is the higher-value step.
- **Round 18–19:** added `paper/reproduce.sh` (one-command repro of E1–E11; keyless offline
  path verified). **Numeric-consistency proofread (Round 19): PASS** — every number in the
  paper (E1 100/96/96, 83/33/0, CIs; E2 89%/83%; the two gpt-4.1 misses; 0/3→2/2→1/1→4/5;
  ~80%) cross-checked against actual experiment outputs; abstract/body/table consistent, no
  contradictions. **Loop paused here** by Claude's judgment: paper is a complete defensible
  draft, autonomous returns are padding from here; next step is user review + local compile
  (no LaTeX engine on box). Re-invoke `/loop` to resume.

## Open threads to settle empirically

- T1: formalization accuracy in isolation (LLM-as-scribe reliability) — bears on C2
- T2: demo of the engine catching a *wrong* encoded rule a human/LLM verdict would miss — bears on C3
- T3: a 2-agent contract sim where the referee is the commitment device — bears on C7
- T4: does the offence-ID / pair gap widen with norm complexity (T1→T4 tiers)? current data too small per tier
