# Per-case labelling protocol (for case-labelling agents)

You are labelling ONE Employment Appeal Tribunal unfair-dismissal case (ERA 1996 ss94-98) for an eval corpus.
Repo: /home/flecart/Desktop/work/deontic (work there). Only create/edit the
files this task produces — touch nothing else. Your dispatch names the CASE
path (like ukftt/grc/2026/845), its title, and a candidate stratum.

1. Run: .venv/bin/python docs/experiments/employment_corpus/fetch_case.py <case-path> --label --out <stem>
   Choose <stem>: short lowercase slug, usually <surname>_v_ic; if several
   cases share a surname, append the FCL number (e.g. greenwood_v_ic_835).
   Read the printed KEEP/HIDE section split carefully.

2. UNSUITABILITY CHECK — delete the case file with an ABSOLUTE path
   (rm -f /home/flecart/Desktop/work/deontic/docs/experiments/employment_corpus/cases/<stem>.md
   ), then VERIFY with ls that it is gone (agents routinely
   claim deletion that never happened), and STOP with final report
   "SKIP <case-path> | <reason>" if: the appeal is not an unfair-dismissal
   liability dispute under ERA 1996 (discrimination-only, wages, contract,
   remedy-only, procedure-only appeals are out of scope), the EAT remitted
   without a standing liability outcome, or there is no clean fair/unfair
   gold. The EAT decides errors of law: gold is the liability outcome that
   STANDS after the EAT decision (upheld ET finding, or substituted finding);
   if liability is left open by remittal, SKIP. Mixed FOIA/EIR
   decisions are kept only if an EIR exception is decisive for the disputed
   information.

3. LEAK CHECK — if tribunal analysis leaked into KEEP (the decision lacks a
   "Discussion"-style umbrella heading; analysis headings with the tribunal's
   own findings appear in KEEP), rerun step 1 adding:
   --withhold-from "<heading where the tribunal's own analysis starts>" --force
   If cache/<slug>_reasoning.txt has NO sections (the tool also prints a
   WARNING), the WHOLE decision landed in KEEP: you MUST fix it — find the
   exact text where the tribunal's own analysis begins and rerun with
   --withhold-from using that text; if no heading text matches (truly
   headingless decision), manually edit the case file: cut everything from the
   start of the analysis to "## Disputed information" out of ## Background and
   append it to the reasoning file, leaving an HTML comment noting the manual
   cut. NEVER leave tribunal findings in ## Background.

4. Read docs/experiments/employment_corpus/cache/<slug>_reasoning.txt (path printed
   by the tool). Verify EVERY drafted label against the tribunal's explicit
   findings and fix docs/experiments/employment_corpus/cases/<stem>.md:

   - ## Gold: "unfair" (the dismissal stands as unfair after the EAT) or
     "fair" (claim fails).
   - ## Gold rules — "engaged:" = rule labels the tribunal found ENGAGED (own
     test met, even if the exemption lost the balance), from exactly:
     r12_4b_exc r12_4c_exc r12_4d_exc r12_4e_exc r12_5a_exc r12_5b_exc
     r12_5c_exc r12_5d_exc r12_5e_exc r12_5f_exc r12_5g_exc r13_exc.
     Empty if none. EVERY reg 12 exception is qualified — engaged means its
     own test is met even if the public-interest balance went to disclosure.
   - "pi:" = maintain | disclose | na — the reg 12(1)(b) balance for the
     decisive exception (remember the reg 12(2) presumption: equipoise =
     disclose); na if nothing engaged or only r13 first-condition decided.
   - ## Oracle facts: comma-separated atoms that hold per the tribunal's
     findings. Read the dictionary FIRST:
     ./.lake/build/bin/deontic atoms examples/employment/employment.ddl
     (each description states its truth conditions — apply them, nothing
     else). Typical fair case: Dismissed, QualifyingService, FairReasonShown,
     ReasonableResponse. Typical unfair case: Dismissed, QualifyingService
     (+ FairReasonShown when the reason was shown but the response was
     unreasonable - then omit ReasonableResponse). NEVER include FindUnfair.
   - "exemptions:" header field: plain text like "s40(2)" (no brackets).
   - Appeal allowed IN PART with distinct fact patterns -> you MUST split into
     <stem>_part_a.md / <stem>_part_b.md (pattern:
     cases/garrard_v_ic_british_museum_part_a.md): one instance for the parts
     ordered disclosed (gold=disclose), one for the parts upheld
     (gold=withhold), each with its own Disputed information, engaged rules,
     and oracle facts. Never label a part-allowed case as one instance whose
     engaged absolute exemptions contradict gold=disclose.

5. SCOPE RULE: gold, engaged rules, and oracle facts describe the DISPUTED
   information ONLY. Material whose withholding was conceded, not contested,
   or resolved separately is out of scope — do not list its exemptions as
   engaged or its atoms as oracle facts (split into parts when two disputed
   bodies have different outcomes).

6. Write a concise ## Disputed information section (what exact information is
   in dispute; for NCND cases say the dispute is whether to confirm or deny).

7. "verified:" header — "yes" ONLY if every label is directly supported by an
   explicit statement in the reasoning file; otherwise "no" plus an HTML
   comment in the file explaining the doubt.

8. Validate: .venv/bin/python docs/experiments/employment_corpus/pipeline.py --case <stem> --arms oracle
   Oracle must score OK on disposition and engaged (consistency of your labels
   with the formal theory). A successful s98 defence yields engine status P(FindUnfair),
   which maps to fair — that is correct. If MISS: re-check
   your labels first; if the mismatch is genuinely an engine/theory
   limitation (e.g. pure NCND dispute scored on the Disclose atom), keep the
   case, set verified: no, and say so in your note.

9. FINAL REPORT — your last message must END with exactly one line:
   "OK <stem> | <citation> | gold=<g> | engaged=<labels or none> | pi=<p> | outcome=<dismissed/allowed/part> | verified=<yes/no> | <one-clause note>"
   or "SKIP <case-path> | <reason>"
