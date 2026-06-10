# Atom precedents — tribunal applications, scoped per atom

Case law as *interpretive guidance attached to one atom*: an entry records how
a tribunal cashed out that atom's test on a concrete fact pattern. When the
ground arm judges an atom, it sees only that atom's entries — a precedent
about "vehicle" touches only `Vehicle`; other cases are irrelevant by
construction.

Division of labour with the atom *description* (the contract, in `foia.ddl`):
the description carries the **settled test** (statute wording + canonical
appellate tests — Three Rivers, the prejudice test, the Art 6(1)(f) limbs);
this file carries **fact-pattern-level applications** that accumulate as the
corpus grows. When an application becomes settled doctrine, consolidate it
into the description (codification) and drop the entry.

Format: `## <Atom>` sections; each entry is `- source: <case-file stem>`
followed by an indented `note:`. The `source` drives **leave-one-out**: the
pipeline never shows a case its own precedent entries (no circularity; entries
from Garrard apply to neither Garrard part).

## ContraveneDPPrinciples

- source: driver_v_ic_thanet
  note: The necessity step failed — so disclosure would contravene the
  data-protection principles — where a detailed PUBLISHED SUMMARY (naming the
  senior officers and replicating key findings) already met the transparency
  interest; disclosing the full investigation report containing personal data
  of employees, councillors, investigators and lawyers exceeded what the
  legitimate interest required ([2025] UKFTT 61 §§16–18).

## PrejudiceCommercialInterests

- source: garrard_v_ic_british_museum
  note: Internal notes revealing an institution's desired outcomes, agenda
  positions and work-in-progress thinking DID prejudice commercial interests
  while sponsorship negotiations were LIVE and at an early "cultivation"
  stage at the response date — timing was critical. But basic biographies of
  high-profile public figures, slide titles, and content already obvious from
  the released parts of the same documents gave a competitor no tangible
  advantage and did NOT prejudice commercial interests
  ([2024] UKFTT 601 §§105–138).

## LegalPrivilege

- source: kennaugh_v_ic
  note: Advice privilege covered communications between an authority's
  IN-HOUSE legal adviser and the authority about how to handle a complainant's
  grievance — the adviser's employment status did not matter, and the material
  did not need to relate to litigation ([2026] UKFTT 790 §§51–56).

## PiMaintainOutweighs

- source: kennaugh_v_ic
  note: Where the engaged exemption was legal professional privilege, the
  inherent public interest in keeping legal advice confidential required
  EXCEPTIONALLY strong countervailing factors; a reasonable suspicion of
  wrongdoing plus the general interest in understanding the authority's
  rationale was not sufficient — the balance favoured maintaining
  ([2026] UKFTT 790 §§64–74).
- source: garrard_v_ic_british_museum
  note: Where the engaged exemption was commercial prejudice, a very strong
  general transparency interest (fossil-fuel sponsorship of a public
  institution) still lost the balance because the SPECIFIC withheld material
  shed only limited light on that debate, while the risk to live negotiations
  was real — weigh the actual contribution of THIS material, not the topic's
  importance ([2024] UKFTT 601 §§139–152).
