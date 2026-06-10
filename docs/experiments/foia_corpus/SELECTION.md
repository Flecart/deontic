# Case selection criteria — FOIA corpus

How cases enter the corpus, so every inclusion is reproducible and every
exclusion is principled. This file is updated as collection proceeds; the
per-case record lives in [`cases.csv`](cases.csv).

## Source and discovery

- **Single source:** Find Case Law (caselaw.nationalarchives.gov.uk),
  First-tier Tribunal (General Regulatory Chamber). Discovery via the Atom
  search feed (`/atom.xml?query=...&court=ukftt%2Fgrc&order=-date`), one query
  per stratum (the query strings are recorded per case in cases.csv). FCL
  serves judgment XML at `<url>/data.xml`; intake is `fetch_case.py`.
- **Licence note:** bulk computational re-use of FCL content may require TNA's
  computational-analysis licence; this corpus is hand-picked research material
  fetched one case at a time with an identifying User-Agent. Resolve the
  licence question before any public redistribution of case texts (the
  *labels and atoms* are ours; the judgment texts are Crown copyright).

## Inclusion criteria

A candidate enters the corpus iff ALL hold:

1. **FOIA disposition.** The appeal decides a Freedom of Information Act 2000
   question (s1 duty vs Part II exemption, or a Part I blocker: s12 cost,
   s14 vexatious/repeated, s9 fees). Pure EIR 2004, pure DPA/GDPR, and
   procedure-only decisions (extensions of time, strike-outs, costs) are
   excluded — recorded as SKIP with reason.
2. **Extractable gold.** The decision states a disposition mappable to
   withhold / disclose at the level of an identifiable body of disputed
   information. Part-allowed decisions are split into per-part instances
   (like Garrard) when the parts have distinct fact patterns; otherwise the
   dominant part is taken and the split noted.
3. **Formalized rules suffice.** The decisive exemption(s) exist in
   `examples/foia/foia.ddl` (after the full Parts I–II formalization this
   excludes almost nothing; the known out-of-scope list: s36 Commons/Lords
   absolute variant, s40 second/third conditions).
4. **Clean intake.** The judgment XML parses, the reasoning/withhold cut is
   verifiable by eye (manual `--withhold-from` where the decision lacks a
   discussion umbrella heading), and the kept background contains enough
   found-fact material to ground the atoms.
5. **"Held or not held" disputes** (authority says it holds nothing, appellant
   disagrees) are included only when an exemption or blocker is ALSO decided;
   pure adequacy-of-search disputes are the fact-finding-only control stratum
   (capped, see below).

## Stratification targets (pilot = 100 instances)

| Stratum | Target | Rationale |
|---|---:|---|
| s40 personal data | 22 | most litigated; absolute-with-internal-test |
| s31 / s30 law enforcement & investigations | 14 | qualified, PI-decisive |
| s43 commercial interests | 12 | qualified, PI-decisive |
| s42 legal professional privilege | 10 | qualified, near-categorical PI |
| s35 / s36 policy & public affairs | 12 | hardest PI balance |
| s14 / s12 procedural blockers | 10 | very common; duty-never-arises semantics |
| absolute exemptions (s21/s23/s32/s41/s44, NCND) | 10 | engine-trivial baseline |
| multi-exemption / depth | 10 | the deduction load |
| fact-finding-only control | ~ (within above) | engine-adds-nothing check |

Outcome mix: aim ≥25% appeals allowed or part-allowed (the subset where
following the ICO's decision notice fails — the discriminative cases).

## Labelling protocol (per case, one agent per case)

1. `fetch_case.py <path> --label` — XML intake, auto section split,
   model-drafted labels (gpt-4.1; the eval should then prefer a different
   model family, or treat drafted labels as suspect until verified).
2. Agent eyeballs the KEEP/HIDE split; sets `--withhold-from` if reasoning
   leaks into the background (no discussion umbrella heading).
3. Agent reads `cache/<slug>_reasoning.txt` and verifies every label against
   the tribunal's stated findings: disposition, engaged rules, PI direction,
   oracle facts. Writes the `## Disputed information` section. Fixes anything
   the draft got wrong.
4. `verified: yes` only when the labels match the tribunal's explicit
   findings; anything doubtful stays `verified: no` with a note and is
   triaged by the coordinator.
5. One agent per case, fresh context — no agent sees another case's
   reasoning, labels, or this coordinator's running tallies.

## Exclusion log

Skipped candidates are recorded in cases.csv with `status=skip` and a reason
(`eir-only`, `dpa-only`, `procedure-only`, `no-clean-gold`, `out-of-scope-rule`,
`intake-failure`, `duplicate`).
