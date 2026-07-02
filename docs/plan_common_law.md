# Project plan — Common Law for Agent Societies

Pivot brief, 2026-07-02. This file is the working contract across machines and
agent sessions: items marked **DECIDED** are settled, items marked **PROPOSED**
need Angelo's steer (§7). Cold-start order: `CLAUDE.md` →
`docs/positioning.md` → this file. The two prior artifacts this plan builds on
are `freight/Report.md` (the pilot) and `eval/README.md` (the static suite).

## 0. Thesis

**DECIDED (direction).** For societies of LLM agents, norms should be shipped
as a **process, not a text**: a thin open-textured statute + an accumulating
body of adjudicated precedent + a formal (defeasible deontic) coherence
monitor. Claim: this *common-law architecture* beats every static drafting of
the same norms — closed enumeration, open intension, hybrid — on the three
things coordination needs:

1. **Epistemic coordination** — distinct agents/models converge on what the
   norm requires (inter-grounder agreement rises with case-store size);
2. **Behavioral coordination** — disputes decay, settlement replaces
   litigation, deterrence binds (society level, freight);
3. **Robustness** — the advantage survives novel cases (Tier 2) and
   adversarial persuasion (sway-style probes).

"Common law works" = wins on all three at matched label/compute budget, with
the known failure mode (error entrenchment) *measured*, not hidden.

## 1. Why this is a contribution (the skeptic ladder)

Each anticipated objection is assigned an experiment:

| Skeptic says | Answer | Where |
|---|---|---|
| "Precedent retrieval is just RAG / few-shot" | The institution, not the trick: *which* cases enter the store is dispute-selected; selection beats uniform sampling at matched size | E2 |
| "Another descriptive tradeoff paper" | E1 delivers a mechanism you can ship: dominance over the static drafting frontier | E1 |
| "Toy simulation" | Gold-by-construction labels; pre-registered predictions from law & economics (Priest–Rubin); a formal instrument (DDL closure) | all |
| "LLM judge errors compound through precedent" | Measured head-on: entrenchment half-life vs stare-decisis strength | E4 |
| "No one can use this" | Packaged governance layer (statute + store + monitor) behind one CLI/API surface | §3 |

Flagship scientific nugget (frame prominently): **litigation is active
learning.** Selection means parties settle clear cases and file ambiguous
ones, so the case store concentrates on the decision boundary — common law is
an *incentive-generated curriculum* the legislator gets for free. E2 tests it
against uncertainty sampling directly. To our knowledge untested anywhere.

**Citation hygiene:** freight's "Priest–Rubin" label conflates two
literatures. The ~50% win-rate *selection* hypothesis is **Priest & Klein
1984**; the *evolutionary efficiency of common law* line is **Rubin 1977 /
Priest 1977**. Cite both correctly; law-and-econ reviewers will check.

### Related-work anchors (the four conversations E1 must join)

1. **Legal NLP tasks** — SARA (statutory subsumption), COLIEE (case
   retrieval + entailment), LegalBench. E1 is recognizably their task; the
   differentiators are the *endogenous* corpus (built by the system's own
   adjudications) and gold-by-construction **retrieval relevance labels**,
   which COLIEE lacks.
2. **AI & Law CBR theory** — HYPO (Ashley), CATO (Aleven), Horty's
   *precedential constraint*, Prakken & Sartor. E1's rule-subsumption
   retrieval (below) operationalizes Horty; follow-vs-distinguish is their
   doctrine, measured.
3. **ML** — RAG, in-context example selection (kNN-ICL line), active
   learning, and the classic **CBR cycle** (Aamodt & Plaza:
   retrieve–reuse–revise–retain — E1 is that cycle with an LLM judge; say
   so, it converts "just RAG" into a 30-year theory conversation).
4. **Alignment / agents** — closest prior: **Case Law Grounding** (Feng et
   al. ~2024 — verify cite): human-authored precedents aligning single
   decisions. Ours: dispute-selected endogenous store, formal coherence
   monitoring, evaluated on *coordination*. Plus Constitutional AI,
   Hadfield-Menell & Hadfield 2019, GovSim et al. (already in positioning).

**RAG vs case law, for the paper's framing:** a precedent is *authoritative*
(binds unless distinguished — E4 measures how binding it should be), the
corpus is *endogenous* (accretion rule = E2's variable), holdings are
*written for reuse* (adjudicator output format is a design surface), the
objective is *inter-decision consistency* not per-query accuracy, and there
is *defeasibility doctrine* (distinguish/overrule — the DDL closure monitor
is its machine form). One-liner: RAG is a memory; case law is a memory with
a constitution.

## 2. Experiments

### E1 — Precedent-augmented grounding beats the static frontier (CORE, gate)

Stream cases (existing banks + newly generated, T ≈ 150–300 per statute)
through grounder arms. Contested / low-confidence cases go to an adjudicator
(strong model, exercising the engine's `[JUDGE]` path for the first time);
its holding {facts, atom decision, rationale} enters the store; the grounder
retrieves top-k precedents at classification time.

- **Arms:** closed / open / hybrid (the static frontier); open+precedent
  (ours); open+uniform-examples at matched store size (RAG ablation);
  open+gold few-shot (ceiling).
- **Retrieval design (ablation within the precedent arm)** — the known hard
  problem (COLIEE Task 1): surface similarity retrieves *narratively* similar
  cases, not *legally* similar ones. Three modes: (a) text-embedding cosine
  on facts (pilot baseline); (b) **atom-overlap** on the extracted atom
  vector; (c) **rule-subsumption** — compile holdings to DDL rules (freight
  already does) and retrieve precedents whose rule fires on the current
  facts (Horty's precedential constraint, operationalized). Backward
  generation gives **gold relevance labels** (precedents sharing the latent
  assignment), so report retrieval P@k per mode — retrieval quality is a
  measured variable, not an assumption, and (a)-vs-(c) with gold relevance
  is a publishable NLP result on its own. Grounder is instructed it *may
  distinguish*; measure over-following.
- **Metrics:** per-tier accuracy vs t; inter-model agreement (κ over the
  cheap panel); abstention calibration on unknowns; retrieval P@k vs gold.
- **Success (gates the rest of the project):** precedent arm closes ≥X% of
  the closed↔open Tier-0/1 gap while retaining ≥Y% of open's Tier-2
  advantage, with positive consistency slope. **PROPOSED X=70, Y=90.**
- **Kill:** if precedent ≤ max(open, closed) on every tier after tuning k and
  adjudicator quality, the mechanism fails → fallback paper is "why precedent
  doesn't transfer to LLM grounding" (publishable, much weaker).
- **Statutes: PROPOSED** expA (deepest ablations), expC (Hart floor /
  concept figure), expF (safety constitution — the over-generalization case
  precedent should fix).
- **Cost:** cheap panel + one strong adjudicator; same order as an expA–F
  rerun.

### E2 — Selection: litigation as active learning

At matched store size n, compare accretion policies: dispute-selected
(model disagreement / party prior divergence), uniform random, oracle
uncertainty sampling (ceiling), recency. Hypothesis: dispute-selected ≈
uncertainty sampling ≫ uniform. Deliverable: sample-efficiency curves
(accuracy and agreement vs n).

### E3-lite — Dyadic accountability episodes (PROPOSED 2026-07-02, pending Angelo's confirm)

Scope option under discussion: **Paper 1 = E1 + E2 + E3-lite + the released
benchmark**, with full-scale E3 (welfare economics, regime comparison) and E4
deferred to a follow-up. Rationale: benchmark + mechanism + selection analysis
is a complete top-venue package at the *law-coordination level*; what it loses
without E3 is the society-level welfare claim, so claims must be scoped to
interpretation-consistency and dyadic accountability (see §5).

E3-lite keeps a *behavioral* result at ~1/10 the cost of full freight: repeated
**two-party episodes** using freight's contract shells and judge, no market.
Per episode: (1) seller decides deviation given precedent-based anticipated
liability; (2) buyer decides whether to **file** given the same store (priors
from retrieval, as in the pilot); (3) adjudication → holding accretes.
Metrics: deterrence (deviation rate vs store maturity), invocation decay,
settlement rate, and closure coherence — i.e. "can LLM agents keep each other
accountable through precedent," measured directly, without welfare
aggregation. Reuses `freight/agents.py` + `judge.py` nearly unchanged.


## 3. Engineering deliverables

- Precedent store module (Python, under `eval/`): holding schema {facts,
  atom, decision, rationale, cites}, embeddings, top-k retrieval — start from
  `freight/corpus.py`.
- Adjudicator harness exercising the engine's `[JUDGE]` surface end-to-end —
  start from `freight/judge.py`.
- Generalize freight's holdings→DDL compiler into a standalone **coherence
  monitor** (closure/stability over any store) — this is the instrument
  contribution.
- Stretch (only after the E1 gate passes): `deontic serve` / MCP tool
  exposing (statute + store + monitor) as a governance layer for other agent
  frameworks.
- **Lean engine: no calculus changes.** Touch only if the JUDGE surface needs
  a flag. The engine's role improves from evaluated object to measuring
  instrument.

## 4. Reuse map

| Existing asset | New role |
|---|---|
| expA–F results | §Motivation: the static-drafting frontier (the impossibility that justifies the mechanism) |
| `gen_cases.py` backward generation | extended to case *streams* with a novelty schedule |
| `freight/` | E3 substrate; `corpus.py` → precedent store; `judge.py` → adjudicator |
| DDL engine | coherence monitor + JUDGE + provenance for holdings |
| expB redraft finding | E4 amendment-policy arm |
| `sway.py` | E3 adversarial probe |
| `QA_PROTOCOL.md` gates | extended to streams (description freeze, leak checks apply unchanged) |

## 5. Claim discipline

- "Precedent-based reasoning" becomes claimable once E1 stores real holdings.
  Still do **not** claim human-style analogical reasoning — the mechanism is
  retrieval + conditioning; say so explicitly.
- Welfare is never reported without coherence (freight pilot lesson).
- Pre-register E3 predictions before scaling; keep the pilot's
  honest-negative reporting style — it is a strength.

## 6. Venue & milestones

**PROPOSED** primary: AAMAS 2027 (deadline historically early Oct — verify)
or an ML-venue agents track (ICLR 2027); COINE/NorMAS workshop for early
feedback; ICAIL 2027 secondary with the AI&Law cut.

**EACL option (verified 2026-07-02):** EACL 2027 is Mar 9–14, Athens; its
only viable ARR cycle closes **Aug 3, 2026**. Feasible *only* as the narrow
E1(+retrieval-ablation) NLP cut — "interpreting open-textured norms with
retrieval over adjudicated cases" — at sprint pace; E3 would not survive *CL
reviewing. Decision rule: if the E1 smoke run gates positively by ~Jul 20,
consider the sprint; otherwise skip (a later ARR cycle → ACL/NAACL 2027
keeps the NLP option open). The full coordination thesis stays AAMAS-shaped
regardless.

Milestones (~1 FTE-agent + Angelo steering):

- **M0** (wk 1): case-stream generator + precedent store + adjudicator wired
  on expA; E1 smoke run.
- **M1** (wks 2–4): E1 full on the three statutes → **GATE review**.
- **M2** (wks 5–6): E2.
- **M3** (wks 6–9): E3 scaled + sway probe (after budget estimate).
- **M5**: paper. The §Motivation draft can start immediately from existing
  expA–F results.

## 7. Open decisions — need Angelo's steer

1. E1 gate numbers X, Y (proposed 70 / 90).
2. Statute subset for E1 (proposed expA, expC, expF).
3. Compute ceiling, especially E3's judge model — gate on a `token_cost.py`
   estimate.
4. Venue/deadline, which drives scope: AAMAS-shaped = E1+E2+E3;


## Ideas for followups
5. Agent identity / reputation in freight: **PROPOSED out of scope** for this
   paper (pilot's honest-limitations list).
6. Lean-native/verification angle: **PROPOSED instrument-only** here; the
   Lean-native question stays a separate track (see `docs/positioning.md`).
