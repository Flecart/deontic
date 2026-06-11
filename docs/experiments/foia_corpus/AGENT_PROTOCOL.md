# Per-case labelling protocol (for case-labelling agents)

You are labelling ONE UK First-tier Tribunal FOIA case for an eval corpus.
Repo: /home/flecart/Desktop/work/deontic (work there). Only create/edit the
files this task produces — touch nothing else. Your dispatch names the CASE
path (like ukftt/grc/2026/845), its title, and a candidate stratum.

1. Run: .venv/bin/python docs/experiments/foia_corpus/fetch_case.py <case-path> --label --out <stem>
   Choose <stem>: short lowercase slug, usually <surname>_v_ic; if several
   cases share a surname, append the FCL number (e.g. greenwood_v_ic_835).
   Read the printed KEEP/HIDE section split carefully.

2. UNSUITABILITY CHECK — delete cases/<stem>.md and STOP with final report
   "SKIP <case-path> | <reason>" if: the decision is not a FOIA disposition
   (pure EIR 2004, pure DPA/GDPR, pensions regulation, procedure-only:
   strike-out, costs, time extension), or there is no clean withhold/disclose
   gold for an identifiable body of disputed information.

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

4. Read docs/experiments/foia_corpus/cache/<slug>_reasoning.txt (path printed
   by the tool). Verify EVERY drafted label against the tribunal's explicit
   findings and fix docs/experiments/foia_corpus/cases/<stem>.md:

   - ## Gold: "withhold" (refusal/NCND upheld, or authority not obliged to
     comply) or "disclose" (disclosure or confirmation ordered). Gold is about
     the DISPUTED INFORMATION, not who wins: if the AUTHORITY appealed an ICO
     disclosure order and lost, gold=disclose.
   - ## Gold rules — "engaged:" = rule labels the tribunal found ENGAGED (own
     test met, even if the exemption lost the balance), from exactly:
     s21_exempt s22_exempt s22a_exempt s23_exempt s24_exempt s26_exempt
     s27_exempt s28_exempt s29_exempt s30_exempt s31_exempt s32_exempt
     s33_exempt s34_exempt s35_exempt s36_exempt s37_royal_exempt
     s37_other_exempt s38_exempt s39_exempt s40_1_exempt s40_2_exempt
     s41_exempt s42_exempt s43_1_exempt s43_2_exempt s44_exempt
     s12_cost s14_vex s14_rep s9_fees.   Empty if none.
   - "pi:" = maintain | disclose | na — the s2(2)(b) balance direction for the
     decisive qualified exemption; na if never reached (absolute exemption,
     nothing engaged, or s12/s14 case — those have no s2(2)(b) balance).
   - ## Oracle facts: comma-separated atoms that hold per the tribunal's
     findings. Read the dictionary FIRST:
     ./.lake/build/bin/deontic atoms examples/foia/foia.ddl
     (each description states its truth conditions — apply them, nothing
     else). Always include Request; HoldsInfo when the disputed information is
     held; ConfirmOrDeny and RefusalNotice when the authority's response
     showed them (in NCND cases ConfirmOrDeny is typically ABSENT). NEVER
     include Disclose, RespondInTime, or AdviseAssist.
   - "exemptions:" header field: plain text like "s40(2)" (no brackets).
   - Appeal allowed IN PART with distinct fact patterns -> you MUST split into
     <stem>_part_a.md / <stem>_part_b.md (pattern:
     cases/garrard_v_ic_british_museum_part_a.md): one instance for the parts
     ordered disclosed (gold=disclose), one for the parts upheld
     (gold=withhold), each with its own Disputed information, engaged rules,
     and oracle facts. Never label a part-allowed case as one instance whose
     engaged absolute exemptions contradict gold=disclose.
   - PURE NCND CASE (the dispute is whether to CONFIRM OR DENY holding, not
     whether to disclose contents): add header line "decision: confirm". Gold:
     withhold = NCND upheld, disclose = confirmation ordered. Engaged rules
     come from the NCND set: s23_ncnd s24_ncnd s30_ncnd s31_3_ncnd s40_5a_ncnd
     sx_ncnd (generic: bare confirmation would cause an engaged exemption's
     harm — use for exemptions without a bespoke NCND rule, e.g. s38(2),
     s43(3)). The PI atom for NCND is PiNcndMaintainOutweighs, NOT
     PiMaintainOutweighs. HoldsInfo is usually UNKNOWN in NCND cases — omit it.

5. SCOPE RULE: gold, engaged rules, and oracle facts describe the DISPUTED
   information ONLY. Material whose withholding was conceded, not contested,
   or resolved separately is out of scope — do not list its exemptions as
   engaged or its atoms as oracle facts (split into parts when two disputed
   bodies have different outcomes).

6. Write a concise ## Disputed information section (what exact information is
   in dispute; for NCND cases say the dispute is whether to confirm or deny).

6. "verified:" header — "yes" ONLY if every label is directly supported by an
   explicit statement in the reasoning file; otherwise "no" plus an HTML
   comment in the file explaining the doubt.

7. Validate: .venv/bin/python docs/experiments/foia_corpus/pipeline.py --case <stem> --arms oracle
   Oracle must score OK on disposition and engaged (consistency of your labels
   with the formal theory). Upheld s12/s14 yield engine status P(Disclose) =
   not obliged, which maps to withhold — that is correct. If MISS: re-check
   your labels first; if the mismatch is genuinely an engine/theory
   limitation (e.g. pure NCND dispute scored on the Disclose atom), keep the
   case, set verified: no, and say so in your note.

8. FINAL REPORT — your last message must END with exactly one line:
   "OK <stem> | <citation> | gold=<g> | engaged=<labels or none> | pi=<p> | outcome=<dismissed/allowed/part> | verified=<yes/no> | <one-clause note>"
   or "SKIP <case-path> | <reason>"
