# FOIA corpus — scoping index

*What we must build to test an LLM judge against real case law on a domain the
engine can actually reason over. Two registers: the **law to formalize** (paid
once) and the **cases to index** (scales the eval). Numbers are grounded where
marked; estimates are flagged.*

Why FOIA: a **closed, shared rulebook** (one statute, ~24 enumerated exemptions)
with a large pool of tribunal decisions that are **rule-application disputes**
(which exemption applies + the public-interest balance), not fact-finding. That
is the sweet spot — see the negative control below for the opposite.

---

## Register A — Law to formalize (the rulebook, paid once)

Source: **Freedom of Information Act 2000**, Parts I–II. The framework is small and
bounded; that boundedness is the whole reason to pick FOIA.

| Module | Provisions | DDL rules (est.) | Kind |
|---|---|---:|---|
| Core duty | s1(1)(a) confirm-or-deny, s1(1)(b) communicate | 2 | default `O(disclose)`, `O(confirm)` |
| Exemption meta-layer | s2 (absolute vs qualified + **public-interest test**), s17 refusal notice, s58 appeal powers | 3–4 | the superiority + balancing layer |
| **Absolute** exemptions | s21, s23, s32, s34, s40(1), s41, s44 | ~7 | each: `F(disclose)` **supreme** over s1 |
| **Qualified** exemptions | s22/22A, s24, s26–s31, s33, s35–s39, s40(2), s42, s43 | ~17 | each: `F(disclose)` **unless** PI in disclosure outweighs |
| NCND (neither confirm nor deny) | s2(1) duty-to-confirm exclusions, per exemption | ~5–8 | stacks on a substantive exemption |
| **Definitions / grounding atoms** | "personal data", "public authority", "prejudice", "investigation", "commercial interests"… | ~25–30 atoms | descriptions, **not** rules — LLM grounds these |

**Totals.** Full framework ≈ **30–40 DDL rules + ~25–30 grounded atoms**.
Pilot subset (5 exemptions) ≈ **12–15 rules + ~15 atoms**.

**Honest boundary.** The open-textured predicates — *"would prejudice"*,
*"public interest"* — are **grounding atoms the LLM judges**, not rules the engine
deduces. The engine owns: absolute-vs-qualified resolution, exemption-defeats-duty,
NCND stacking, multi-exemption interaction. Keep the split visible (it's the whole
grounding-vs-deduction attribution we need for the eval).

---

## Register B — Cases to index (scales the eval)

**Pool (grounded):** ~13,500 First-tier Tribunal (General Regulatory Chamber)
decisions on Find Case Law (271 pages × 50/page, queried 2026-06-10). Information
Rights (FOIA/EIR/DPA appeals) is the dominant subset → **several thousand**
FOIA-relevant decisions available, freely, under the Open Justice Licence.
Supply is **not** the constraint; labelling effort is.

**Gold = the tribunal disposition** (appeal *dismissed* → exemption upheld /
*allowed* → disclosure ordered / *part*). External, human, non-circular.

**Sampling plan (stratified by dominant exemption + outcome):**

| Stratum | Purpose | Cases |
|---|---|---:|
| s40 personal data | most common; absolute+qualified mix, NCND | 25–30 |
| s31 law enforcement / s30 investigations | qualified, PI test | 25–30 |
| s43 commercial interests | qualified, PI test | 25–30 |
| s42 legal professional privilege | qualified, strong-default PI | 20–25 |
| s35/s36 govt policy & public affairs | qualified, hardest PI balance | 20–25 |
| **Depth stratum**: multi-exemption / PI-decisive | the deduction load | 25–30 |
| Control: absolute-exemption easy cases | engine-trivial baseline | ~15 |
| Control: fact-finding-only appeals | **engine-adds-nothing** baseline | ~15 |

**Targets.** Pilot ≈ **150 cases indexed / ~125 scored** (5 exemptions, ~25 each
for usable per-exemption Wilson CIs). Full study ≈ **~350–400 cases** (10
exemptions × 30 + depth stratum).

**Per-case labelling cost.** (a) extract found facts → atoms [LLM pre-extract +
human spot-check], (b) record exemption(s) claimed, (c) record disposition [gold].
≈ **15–30 min/case** verified; (b)+(c) are near-mechanical, (a) is the labor.

**Index columns** → see [`cases.csv`](cases.csv).

---

## Negative control (already read)

`[2026] EWFC 131` *FAZ v MAZ* (Family, sexual-abuse fact-finding): clear gold,
clear reasoning, but the dispute is *what happened*, not *which rule applies* —
~0% deduction. Keep it as the canonical "engine adds nothing here" case so the
eval shows where the tool **doesn't** help, not only where it does.

---

## Phased plan

- **Phase 0 — feasibility (~1 day).** Formalize duty + s40 path (~6 rules); index
  the 5 seeded s40 cases end-to-end; confirm the engine reaches each disposition.
- **Phase 1 — pilot (~1–2 wks).** 5 exemptions, ~15 rules, ~125 scored cases;
  LLM-only vs LLM+engine, accuracy split into grounding vs deduction error.
- **Phase 2 — full (~1 mo).** ~35 rules, ~350 cases, depth stratum drives the
  "widening gap" curve.

**Bottom line on the question asked.** Law to formalize: **~30–40 rules** (one
statute), pilot-able with **~15**. Cases to index: pool is thousands; we need
**~125 for a pilot, ~350 for the full study** — labelling, not access, is the cost.

---

## Phase 0 artifacts (built 2026-06-10)

- **Formalization:** `examples/foia/foia.ddl` — s1 duties, s2 layer, s17
  notice, NCND, five exemptions (s21/s31/s40/s42/s43); 13 rules, 16 atoms;
  `examples/foia/tests.sh` is 16/16 green.
- **Cases:** [`cases/`](cases/) — *Driver v IC & Thanet DC* [2025] UKFTT 61
  (s40(2), dismissed); *Garrard v IC & British Museum* [2024] UKFTT 00601
  (s43(2), allowed **in part** — encoded as two instances, Part A withhold /
  Part B disclose, i.e. gold at the per-part level as the sampling plan needs);
  *Kennaugh v IC* [2026] UKFTT 790 (s42(1), dismissed — decided May 2026, past
  current model cutoffs, so memorization-free); *Logan v IC & Home Office*
  [2025] UKFTT 393 (s40(2)+s38(1), allowed **in part** — Part A withheld:
  special-category IRA data, Article 6(1)(f) balance data subjects win,
  fingerprint/medical; Part B disclosed: Balcombe Street ASU confessors via
  Article 9(2)(e), deceased individuals, public-domain data; manual KEEP/HIDE
  cut required — XML has a single "Introduction" section with no structural
  heading break).
- **Intake tool:** [`fetch_case.py`](fetch_case.py) — Find Case Law serves
  every judgment as Akoma Ntoso XML at `<judgment-url>/data.xml` (**no PDF
  parsing needed**); the tool fetches + caches the XML, splits sections in
  document order (bold-span headings included — FCL marks few real
  `<heading>`s), withholds everything from the discussion heading onward into
  `cache/*_reasoning.txt` (gold-labelling only, never prompt material), and
  scaffolds a draft `cases/*.md` for human curation. Kennaugh took ~15 min
  fetch-to-green. Old pre-FCL tribunal decisions are PDF-only — add a PDF
  fallback only when a sampled case forces it.
- **Run viewer:** [`frontend/`](frontend/) + [`app.py`](app.py) — React UI
  (sidebar run list, score dashboard, per-case pred/gold, atom-failure
  reasoning, prompt inspector). `cd frontend && npm run dev` →
  http://localhost:5174
- **Pipeline:** [`pipeline.py`](pipeline.py) — three arms (oracle facts→engine,
  LLM-grounds→engine, LLM-only) against OpenAI models, scored on **four
  dimensions**: disposition, exemption-rule engagement (gold in each case
  file's `## Gold rules`), the s2(2)(b) PI direction, and (ground arm)
  **per-atom facts agreement** vs the verified oracle facts — the sensitive
  endpoint (15 judgments/case instead of 1). Engine arms read rule selection
  off the `query --why` proof certificate.
- **Design decisions (2026-06-10 revision):**
  - *Backgrounds are the raw kept sections* from the judgment XML, not
    hand-curated summaries — curation was a selection-bias / researcher-DoF
    risk; procedural noise hits both model arms equally.
  - *Labels are model-drafted, human-verified*: `fetch_case.py --label` has a
    model transcribe oracle facts + gold from the withheld reasoning (it is
    transcription — the tribunal states its findings explicitly; validated:
    the draft reproduced the hand labels for Kennaugh exactly). Case files
    carry `verified: yes|no`; the pipeline skips unverified cases. Use a
    **different model family** for drafting than the one evaluated, so label
    noise can't correlate with the system under test.
  - *`--atoms-per-call K`* (with `--seed` for batch composition) is a design
    parameter of the ground arm: how many atoms the model judges per call
    (0 = all). Batches are independent — the case text itself carries
    inter-atom context (it names the claimed exemption), so no batch needs
    another's output. This sweeps the spectrum from the llm arm (holistic) to
    fully decomposed grounding.
  - *Withhold cut is human-checked*: decisions without a "Discussion" umbrella
    heading (Driver) need `--withhold-from`; the tool prints the KEEP/HIDE
    split for the 30-second review.
  - *Every call is logged*: each pipeline invocation writes
    `runs/run_<stamp>_<arms>.jsonl` — `run_meta`, one `llm_call` per API call
    (full prompts, raw reply, tokens, latency, batch composition), one
    `arm_result` per case×arm. [`view_run.py`](view_run.py) displays a run;
    `--failures` joins each missed/extra atom to the model's own reasoning.
- **First failure taxonomy from the logs (gpt-4.1, K=all):**
  (1) *relevance filtering* — the model deliberately omits true procedural
  atoms ("RefusalNotice … is not determinative in the tribunal's outcome"): it
  answers "does it matter", not "does it hold" — a GROUND_SYSTEM prompt fix
  candidate; (2) *confabulated evidence* — on Garrard B it justified
  PrejudiceCommercialInterests with "the closed evidence shows…", citing a
  closed bundle it has never seen; (3) *part-scoping bleed* — whole-case
  submissions applied to the disputed subset.

## Instrument v2 (2026-06-11): truth-conditional atoms + atom-scoped precedents

Two changes targeting the failure taxonomy; *the description IS the test* by
design — what establishes an atom's truth must live in its description.

- **Truth-conditional descriptions** (`examples/foia/foia.ddl`): every atom
  now states when it is TRUE / FALSE — the settled tests are in the contract
  (the privilege limbs, the causative-link/real-prejudice test, the
  legitimate-interest/necessity/balancing steps, at-the-time framing and
  specific-material weighing for the PI balance; procedural atoms say "assert
  even if not determinative"). Settled doctrine → description; fact-pattern
  applications → precedents (consolidate upward when an application becomes
  settled, like codification). **Descriptions are self-contained — no
  references**: never "the s40(3A) first condition" or "(Three Rivers)"; the
  reader has neither the statute nor the other atoms (batching can isolate an
  atom completely), so the test's content is inlined verbatim. Rule codified
  in `eval/deontic_skill.md` §Writing atom descriptions.
- **Atom-scoped precedents** (`examples/foia/precedents.md`, pipeline
  `--precedents`): case law attached to *one atom* — when grounding an atom
  the model sees only that atom's entries ("vehicle in the park" touches only
  `Vehicle`; other cases are irrelevant by construction). **Leave-one-out by
  source case**: a case never sees entries derived from itself (Garrard parts
  share a source stem). Utility grows with the corpus; with 3 source cases
  most entries are blocked for their own case and thin for others.
- **GROUND_SYSTEM hardened**: judge only from the supplied background (no
  closed-material confabulation); assert every atom whose test is satisfied,
  procedural or not.
- **Results (gpt-4.1, K=all, single runs — note identical configs varied
  55–57/60 across reruns, so ±2 facts is run noise; claims need repeated
  seeds):** v1 baseline facts 55/60 → v2 57/60 (procedural misses gone) → v2 +
  precedents **59/60, disposition 4/4** (Garrard B fixed). Residual failure is
  a new class: (4) *cross-atom contamination* — Driver's published-summary
  evidence correctly drives ContraveneDPPrinciples (necessity fails) but
  bleeds into AccessibleOtherMeans ("the summary is published so the report is
  accessible"), contradicting the description's explicit exclusion. The
  targeted cure is exactly an s21 precedent from a *future* case
  (leave-one-out blocks Driver's own); also interacts with the
  atoms-per-call parameter (would isolation stop the bleed?).
- **Raw-background results (gpt-4.1, n=4):** ground at K=all: disposition 3/4,
  engaged 3/4, facts 56/60; at K=4: disposition 3/4, engaged 2/4, facts 54/60.
  Two early observations: (1) **Garrard Part B flipped to a miss** under raw
  backgrounds — parts A and B share one background and differ only in the
  disputed-information description, and the model let the Museum's
  whole-case submissions bleed into the part-B subset (curated backgrounds had
  masked this; raw is harder but fairer — scoping the judgment to the disputed
  subset is part of the task). (2) **Smaller batches added false-positive
  atoms** (s21 for Driver — the Public Summary is accessible, the unredacted
  report is not; stray PI atoms): atoms judged in isolation lose the implicit
  exclusivity of seeing the full dictionary at once. n=4 is plumbing-scale —
  these are hypotheses for the pilot, not findings.
- **First results (gpt-4.1, n=4):** Kennaugh (easy-qualified s42: the LPP
  balance is near-categorical) — all arms correct on all dimensions, a useful
  contrast stratum to Garrard A. On the original three instances: on
  disposition alone all arms were 3/3 —
  the saturation the headroom risk predicted. Rule-level scoring broke it:
  LLM-only **missed the Garrard A public-interest balance** (called it for
  disclosure; the tribunal — and the structured ground→engine arm — called it
  for maintaining). Same model, holistic vs atom-by-atom prompting, opposite
  PI judgments on a balance the Commissioner had called "finely balanced".
  n=1, but exactly the signal the pilot should chase: score *grounding
  decomposition* and *structure*, not bare outcomes.
