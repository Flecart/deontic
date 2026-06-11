# Domain replications — FOIA-equivalents for the formalization dataset

Goal: 7–8 statute/rulebook formalizations with real-case eval corpora, same
paradigm as `foia_corpus/`: closed rulebook → DDL theory; published decisions
→ verified gold; three-arm eval (oracle / ground / llm). Selection criteria
for a GOOD domain (inherited from FOIA's INDEX.md rationale):

1. **Closed, bounded rulebook** — one statute/regulation set, enumerable
   tests; the engine can own the whole structural layer.
2. **Rule-application disputes** — decisions turn on *which rule applies and
   how its open-textured test cashes out*, not on contested primary facts.
3. **Machine-readable decision pool** — bulk, structured, freely accessible,
   with extractable disposition gold.
4. **Outcome diversity** — both directions occur often enough to beat
   base-rate baselines.

## The shortlist (ordered by execution cost)

| # | Domain | Rulebook | Case source | Why / cost notes |
|---|--------|----------|-------------|------------------|
| 1 | **EIR 2004** (UK environmental information) | regs 5, 12(4)(a–e), 12(5)(a–g), 13 | **same FCL feed, same tribunal, same XML intake tool** | The sibling regime: presumption in favour of disclosure (reg 12(2) — a real structural difference from FOIA), exceptions + PI test. **9 cases already fetched & cached** (our FOIA skips: wood_784, parker_339, marney_714, marshall_760, cardin_365, mishiku_698, driver_737, michaels_612, calderbank_490). Near-zero intake cost. |
| 2 | **FTT (Tax) penalty appeals** | VATA 1994 / FA 2009 Sch 55–56: late filing/payment penalties, "reasonable excuse", special circumstances | FCL `ukftt/tc` — **same XML intake tool verbatim** | Massive volume, formulaic structure (penalty engaged? excuse? proportionality), clean dismissed/allowed gold. |
| 3 | **UKIPO trade mark oppositions** | TMA 1994 s5(1)/(2)/(3)/(4), s3 absolute grounds | UKIPO decisions database (O/xxx/yy), free HTML/PDF | Highly formulaic decisions (global appreciation test, comparison of goods/marks); opposition succeeds/fails per ground = per-rule gold. |
| 4 | **Employment: unfair dismissal** | ERA 1996 ss94–98(4): qualifying period, fair reason taxonomy, band of reasonable responses, Polkey | ET decisions on gov.uk (HTML), EAT on FCL | The s98(4) reasonableness test is the PI-balance analogue; fair-reason selection is the exemption-selection analogue. |
| 5 | **Social security: PIP appeals** | WRA 2012 + SSPIP Regs 2013 Sch 1: descriptor point-scoring (daily living/mobility) | UT(AAC) on FCL; FTT(SSCS) sparse | The most engine-friendly rulebook anywhere: explicit additive scoring thresholds (8/12 points). Grounding = descriptor judgments. |
| 6 | **US FOIA** (5 U.S.C. § 552) | nine exemptions + foreseeable-harm standard | CourtListener / RECAP API (free, JSON) | Cross-jurisdiction replication of the flagship — strongest dataset story; segregability analogous to part-splits. |
| 7 | **Financial Ombudsman decisions** | FCA DISP + sector rules (e.g. CONC for affordability complaints) | FOS decisions database (bulk, structured) | Huge volume, uphold/not-uphold gold; pick ONE complaint family (e.g. irresponsible lending) to keep the rulebook closed. |
| 8 | **London parking adjudication** (reserve) | TMA 2004 + contravention code schedule | London Tribunals register | Ultra-formulaic; reserve if any of 1–7 disappoints on access. |

## Execution order

EIR first (free seed corpus + shared tribunal), then FTT-Tax penalties
(same intake tool), then trademarks, then one of employment/PIP, then US
FOIA, then FOS. Each domain repeats the FOIA recipe: sources/*.md with
verbatim quotes → self-contained truth-conditional atoms (per
eval/deontic_skill.md) → rules + tests.sh → AGENT_PROTOCOL-driven per-case
labelling with verified gold → three-arm eval → REPORT.md. Each gets its own
`examples/<domain>/` + `docs/experiments/<domain>_corpus/`.

## Verification debt (flagged, not yet done)

- Confirm FTT(Tax) and UT(AAC) XML availability via `/data.xml` on FCL (one
  fetch each).
- Confirm UKIPO/FOS/ET bulk access terms (the Open-Justice-Licence question
  recurs per source).
- US FOIA: pick the court slice (D.D.C. dominates) and check RECAP coverage.

## First per-domain eval results (gpt-4.1, single runs)

| domain | n | oracle disp. | ground disp. | llm disp. | ground facts |
|---|---|---|---|---|---|
| FOIA 2000 | 101 | 97.0% | 78.2% | 82.2% | 97.0% (43 atoms) |
| EIR 2004 | 16 | 16/16 | **15/16** | 13/16 | 299/304 = 98.4% (18 atoms) |
| FA09 Sch 55 | 7 | 7/7 | 6/7 | 6/7 | 41/42 (6 atoms) |

Cross-domain pattern — now a three-point dose-response on the groundable-atom
universe size: at 6 atoms (tax) the engine arm matches holistic judgment
(6/7 vs 6/7); at 18 atoms (EIR) the engine arm WINS (15/16 vs 13/16 — the
structured PI-presumption layer pays off while per-atom accuracy stays 98%);
at 43 atoms (FOIA) per-atom noise compounds through conjunctive rule bodies
and holistic judgment wins on outcomes (78% vs 82%). The implied claim: the
formal layer beats holistic judgment exactly while grounding error stays
below the compounding threshold set by rule-body width — and its auditability
(proof certificates, attributable errors) is constant regardless. Caveats:
single runs, small n for EIR/tax, EIR/tax labels drafted by the evaluated
model family (agent-verified).
