# Outline — "Common Law for Agent Societies" (working map, 2026-07-03)

Target: AAMAS 2027 primary (plan §6). This file maps each section to its
existing source material so the .tex pass assembles rather than invents.
Numbers cited here are reproduced from committed logs (see
`eval/expA/REPORT_E1E2.md` for provenance).

## 1. Introduction

Thesis: for societies of LLM agents, norms should ship as a **process, not a
text** — thin open-textured statute + dispute-selected precedent + formal
coherence monitor. One-liner for the RAG skeptic: *RAG is a memory; case law
is a memory with a constitution* (plan §1).

Hook sequence: (a) static drafting frontier is a measured impossibility
(closed decays on novelty, open never anchors — source: content.tex RQ1a
aggregate, 6 statutes); (b) the common-law architecture closes the gap in
principle (goldfs ceiling beats both poles, +9.2pp over closed, CI [4.0,14.0]);
(c) what stands between principle and practice is *institutional design*,
which we measure: selection (E2), bindingness (override ladder), coherence
(transmission coda).

## 2. Related work (the four conversations, plan §1)

1. Legal NLP (SARA/COLIEE/LegalBench) — differentiators: endogenous corpus +
   gold retrieval-relevance labels (COLIEE Task 1 lacks them).
2. AI&Law CBR (HYPO/CATO, Horty's precedential constraint) — our
   rule-subsumption retrieval mode operationalizes Horty; follow/distinguish
   measured (v4→v5: 4/16→12/16).
3. ML: RAG / kNN-ICL / active learning / Aamodt-Plaza CBR cycle — E1 is the
   cycle with an LLM judge; E2 is the active-learning claim tested.
4. Alignment/agents: Case Law Grounding (Feng et al. — verify cite),
   Constitutional AI, Hadfield-Menell & Hadfield 2019, GovSim.
   Citation hygiene: Priest & Klein 1984 (selection) ≠ Rubin 1977/Priest 1977
   (evolutionary efficiency) — cite both correctly (plan §1).

## 3. Setup

Backward generation → gold-by-construction labels + gold relevance
(`assign_key`); the DDL engine as verdict layer (findings→verdict is
mechanized; models only ground facts). Stream protocol, dispute detection =
outcome divergence (Priest-Klein filing condition), sonnet-5 adjudicator.
Source: REPORT §Setup + eval/README §E1. Statute: expA (expC/expF ports are
the planned replication — flag as such honestly).

## 4. E1 — precedent vs the static frontier

- F2 table (+5.8pp over open and over uniform, CIs clear).
- F4 κ table: open *diverges* over the stream (0.54→0.45), precedent
  converges (0.74→0.79). THE epistemic-coordination result.
- F5 retrieval ablation w/ gold P@5: embed 11 / atom 27 / rule 13 / gold 73 —
  the "narrative vs legal similarity" measurement; the publishable NLP nugget.
- Honest gate miss + decomposition into retrieval × holding-quality (F3).

## 5. E2 — litigation as active learning

- Sample-efficiency table; dispute monotone to 94.4% @ n=39, > uniform
  seed-max at every n≥5 (3 seeds), ≥ oracle error-sampling; κ→0.899.
- Recency staleness; the incentive-generated-curriculum frame.

## 6. The institution is the treatment (the override ladder) — likely §5-6 merge or own section; this is the paper's most novel material

- Error anatomy → one epistemic-bar atom carries the tax; emergent
  transformed-product doctrine (97% follow, 0 flips) = harmless judicial
  legislation, citation-traceable.
- v1–v6 ladder table: cases > text; bindingness > availability; visibility >
  retrieval; over-following appears at the top rung (consent 7→16).
- Coda: better judge ≠ better society — coherence (0.875 vs 0.56) is the
  transmission mechanism; adjudicator objective = accuracy × coherence.
- Governance readings: judge-model selection is constitutional; stronger
  party writes the precedent (49/5 win shares under asymmetric capability);
  bootstrap trap (judiciary-wide priors can't self-correct endogenously).

## 7. E3-lite (PENDING — gate for paper completeness, plan §2)

Dyadic accountability episodes on freight shells. Not run. Decide with
Angelo whether Paper 1 ships without it (scope to interpretation-consistency
+ dyadic accountability) or waits.

## 8. Limitations & claim discipline

From REPORT §Limitations + positioning: no human-style analogical reasoning
claim (retrieval + conditioning); single statute so far; narrator confound;
asymmetric dispute pair; welfare never without coherence.

## Open writing decisions (Angelo)

1. Venue cut: AAMAS full vs EACL-narrow (E1+retrieval ablation+ladder) — ARR
   closes Aug 3; the ladder strengthens the NLP cut beyond the plan's
   original estimate.
2. Does the override ladder become the headline (it is the most novel
   result) or stay §Follow-up to keep E1/E2 primary?
3. content.tex (static-suite paper): mine for §Motivation, then freeze or
   maintain as separate AI&Law submission?
