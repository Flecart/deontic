# Per-case labelling protocol (for case-labelling agents)

You are labelling ONE UK First-tier Tribunal EIR 2004 case for an eval corpus.
Repo: /home/flecart/Desktop/work/deontic (work there). Only create/edit the
files this task produces — touch nothing else. Your dispatch names the CASE
path (like ukftt/grc/2026/845), its title, and a candidate stratum.

1. Run: .venv/bin/python docs/experiments/eir_corpus/fetch_case.py <case-path> --label --out <stem>
   Choose <stem>: short lowercase slug, usually <surname>_v_ic; if several
   cases share a surname, append the FCL number (e.g. greenwood_v_ic_835).
   Read the printed KEEP/HIDE section split carefully.

2. UNSUITABILITY CHECK — delete cases/<stem>.md and STOP with final report
   "SKIP <case-path> | <reason>" if: the decision is not an EIR 2004
   disposition (pure FOIA, pure DPA/GDPR, pensions regulation, procedure-only:
   strike-out, costs, time extension), or there is no clean withhold/disclose
   gold for an identifiable body of disputed information. Mixed FOIA/EIR
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

4. Read docs/experiments/eir_corpus/cache/<slug>_reasoning.txt (path printed
   by the tool). Verify EVERY drafted label against the tribunal's explicit
   findings and fix docs/experiments/eir_corpus/cases/<stem>.md:

   - ## Gold: "withhold" (refusal/NCND upheld, or authority not obliged to
     comply) or "disclose" (disclosure or confirmation ordered). Gold is about
     the DISPUTED INFORMATION, not who wins: if the AUTHORITY appealed an ICO
     disclosure order and lost, gold=disclose.
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
     ./.lake/build/bin/deontic atoms examples/eir/eir.ddl
     (each description states its truth conditions — apply them, nothing
     else). Always include Request and (when the material is environmental)
     IsEnvironmentalInfo; HoldsInfo when the disputed information was held at
     the request date; RefusalNotice when the refusal cited an exception.
     NEVER include Disclose.
   - "exemptions:" header field: plain text like "s40(2)" (no brackets).
   - Appeal allowed IN PART with distinct fact patterns -> you MUST split into
     <stem>_part_a.md / <stem>_part_b.md (pattern:
     cases/garrard_v_ic_british_museum_part_a.md): one instance for the parts
     ordered disclosed (gold=disclose), one for the parts upheld
     (gold=withhold), each with its own Disputed information, engaged rules,
     and oracle facts. Never label a part-allowed case as one instance whose
     engaged absolute exemptions contradict gold=disclose.

5. Write a concise ## Disputed information section (what exact information is
   in dispute; for NCND cases say the dispute is whether to confirm or deny).

6. "verified:" header — "yes" ONLY if every label is directly supported by an
   explicit statement in the reasoning file; otherwise "no" plus an HTML
   comment in the file explaining the doubt.

7. Validate: .venv/bin/python docs/experiments/eir_corpus/pipeline.py --case <stem> --arms oracle
   Oracle must score OK on disposition and engaged (consistency of your labels
   with the formal theory). A not-held or not-environmental case yields engine status
   P(Disclose) = no duty, which maps to withhold — that is correct. If MISS: re-check
   your labels first; if the mismatch is genuinely an engine/theory
   limitation (e.g. pure NCND dispute scored on the Disclose atom), keep the
   case, set verified: no, and say so in your note.

8. FINAL REPORT — your last message must END with exactly one line:
   "OK <stem> | <citation> | gold=<g> | engaged=<labels or none> | pi=<p> | outcome=<dismissed/allowed/part> | verified=<yes/no> | <one-clause note>"
   or "SKIP <case-path> | <reason>"
