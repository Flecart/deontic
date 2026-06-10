# Freedom of Information Act 2000 — full Parts I–II formalization
# ---------------------------------------------------------------------------
# Scope: the s1 access duties, the s2 absolute/qualified exemption layer, the
# s17 refusal notice, the s10/s16 administrative duties, the Part I duty
# blockers (s9 fees, s12 cost limit, s14 vexatious/repeated — DEFEATERS: they
# remove the obligation rather than forbid the act, so the status becomes
# "not obliged" P, not F), every Part II exemption s21–s44, and NCND for the
# litigated set (s23, s24, s30, s31, s40; the other duty-to-confirm
# exclusions exist in the statute but are folded — add per-case when needed).
# s36's absolute variant (Commons/Lords-held information) and s40's second and
# third conditions are deliberately out of scope at this altitude.
#
# Division of labour (the grounding-vs-deduction split):
#   * GROUNDING atoms — open-textured predicates a tribunal (or LLM fact-finder)
#     judges from the evidence: "would prejudice", "would contravene the DP
#     principles", "public interest in maintaining outweighs". They enter as
#     facts; the engine never derives them.
#   * The ENGINE owns the structure: exemption-defeats-duty (s2), absolute vs
#     qualified, NCND stacking, the s17 notice consequence, multi-exemption
#     interaction.
#
# Encoding choices (surfaced, per repo convention):
#   * Each exemption is a defeasible counter-rule `=>O@Authority ~Disclose`
#     made superior to the s1 duty — the s2(2) effect. A QUALIFIED exemption
#     carries `PiMaintainOutweighs` in its body, so it simply never fires when
#     the public-interest balance favours disclosure (no judge needed); an
#     ABSOLUTE exemption fires on engagement alone.
#   * s40(2) is modelled as ABSOLUTE via the first condition (s2(3): "section
#     40(1) and 40(2) where the first condition is satisfied"); the DP-principles
#     test is the grounding atom ContraveneDPPrinciples, NOT the FOIA PI test.
#   * ONE shared PiMaintainOutweighs atom across qualified exemptions. Tribunals
#     balance per-exemption; a multi-exemption case where the balance differs
#     per exemption needs per-exemption PI atoms (deferred to v2).
#   * s31(1)(a)-(i) purposes are collapsed into one engagement atom (the right
#     altitude for disposition-level eval; `oneof[...]` can split them later).
#
# Facts are scenario-specific (empty default; pass --assume or see
# docs/experiments/foia_corpus/cases/).
facts:

# ---------------------------------------------------------------------------
# Core duty atoms (s1, s17)
# ---------------------------------------------------------------------------
atom Request: a person has made a written request for information to the public authority. TRUE whenever the case shows a freedom-of-information request was made (virtually every appeal); procedural, but assert it when it holds | quote: Any person making a request for information to a public authority is entitled | uri: examples/foia/sources/foia_2000.md#L10-L13
atom HoldsInfo: the authority holds recorded information answering the request, judged for the DISPUTED information. TRUE if the disputed information exists and is held by the authority, even though withheld; FALSE only if the authority does not hold it | quote: whether it holds information of the description specified in the request | uri: examples/foia/sources/foia_2000.md#L10-L13
atom Disclose: the authority communicates the disputed information to the applicant. The decision atom — never assert it as a fact | quote: to have that information communicated to him | uri: examples/foia/sources/foia_2000.md#L10-L13
atom ConfirmOrDeny: the authority has informed the applicant whether it holds the requested information. TRUE when the response revealed whether the information is held — a refusal citing an exemption over held information confirms holding; FALSE only where the authority refused to say whether it holds the information. Procedural, but assert it when it holds | quote: to be informed in writing by the public authority whether it holds information | uri: examples/foia/sources/foia_2000.md#L10-L19
atom RefusalNotice: the authority gave the applicant a written notice stating that it relies on an exemption, which exemption, and why. TRUE whenever the refusal cited an exemption — assert it even though it is procedural and not determinative of the outcome | quote: states that fact, specifies the exemption in question | uri: examples/foia/sources/foia_2000.md#L42-L45

# ---------------------------------------------------------------------------
# Exemption-engagement atoms — GROUNDING layer (judged from evidence, not derived)
# ---------------------------------------------------------------------------
atom AccessibleOtherMeans: the DISPUTED information itself is reasonably accessible to the applicant by means other than this request — already published, available to them under another statutory access regime, or available through the authority's publication scheme (possibly on payment). FALSE when only a summary, a part, or a related document is available: accessibility of a DIFFERENT document does not count | quote: Information which is reasonably accessible to the applicant otherwise than under section 1 | uri: examples/foia/sources/foia_2000.md#L49-L53
atom PrejudiceLawEnforcement: disclosure of the disputed information would, or would be likely to, prejudice the prevention or detection of crime, the apprehension or prosecution of offenders, the administration of justice, the assessment or collection of any tax, the operation of immigration controls, or the maintenance of security and good order in prisons. TRUE only where the background shows a causative link between THIS disclosure and prejudice that is real, actual or of substance, with a real and significant risk of it occurring; FALSE on bare assertion | quote: would, or would be likely to, prejudice | uri: examples/foia/sources/foia_2000.md#L57-L61
atom ConfirmPrejudiceLawEnforcement: merely CONFIRMING OR DENYING that the information is held would itself be likely to prejudice one of those law-enforcement matters (prevention or detection of crime, apprehension or prosecution of offenders, administration of justice, tax collection, immigration controls, order in prisons) — distinct from any harm done by disclosing the contents themselves | quote: compliance with section 1(1)(a) would, or would be likely to, prejudice | uri: examples/foia/sources/foia_2000.md#L63-L65
atom ApplicantOwnData: the disputed information is personal data of which THE APPLICANT THEMSELVES is the data subject — information about the very person who made the request. FALSE when the data is about other people | quote: personal data of which the applicant is the data subject | uri: examples/foia/sources/foia_2000.md#L69-L71
atom ThirdPartyPersonalData: the disputed information constitutes personal data of identifiable living individuals other than the applicant — it relates to them and is biographical in a significant sense. TRUE even for senior officials or public figures; their seniority affects the separate question whether disclosure would contravene the data-protection principles (the ContraveneDPPrinciples atom), not this one | quote: personal data of another person | uri: examples/foia/sources/foia_2000.md#L73-L74
atom ContraveneDPPrinciples: disclosing the third-party personal data to a member of the public would contravene a data-protection principle — chiefly the requirement that processing be lawful and fair: public disclosure of personal data is lawful only when it is necessary for a legitimate interest pursued by the requester or the public, and that interest is not overridden by the data subjects' own interests, rights and freedoms. Apply three steps: (i) is there a legitimate interest in disclosure; (ii) is disclosing THIS material NECESSARY for that interest — necessity fails (and this atom is TRUE) if a less intrusive means, such as an already-published summary, already serves the interest; (iii) if necessary, do the data subjects' rights and reasonable expectations override the interest. FALSE where the legitimate interest genuinely requires this very material and outweighs the subjects' rights (e.g. data the subjects already made public themselves) | quote: would contravene any of the data protection principles | uri: examples/foia/sources/foia_2000.md#L76-L78
atom LegalPrivilege: a claim to legal professional privilege could be maintained over the disputed information in legal proceedings. Advice privilege requires a confidential communication between a lawyer and their client, the lawyer acting in a professional legal capacity (employed in-house counsel counts), made for the sole or dominant purpose of giving or obtaining legal advice; litigation privilege instead covers confidential material whose dominant purpose is use in actual or reasonably contemplated litigation. FALSE if confidentiality has been lost or the dominant purpose was not legal advice or litigation | quote: a claim to legal professional privilege | uri: examples/foia/sources/foia_2000.md#L86-L88
atom TradeSecret: the disputed information itself constitutes a trade secret — technical or commercial information (a formula, process, customer list, pricing method) whose value depends on its secrecy. Narrow: FALSE for ordinarily commercially-sensitive material, which belongs to the separate commercial-prejudice atom (PrejudiceCommercialInterests) | quote: Information is exempt information if it constitutes a trade secret | uri: examples/foia/sources/foia_2000.md#L92
atom PrejudiceCommercialInterests: disclosure of the disputed information would, or would be likely to, prejudice the commercial interests of any person, including the authority itself — harm to someone's ability to participate competitively in commercial activity. TRUE only where the background shows a causative link between THIS disclosure (judged at the time of the authority's response) and prejudice that is real, actual or of substance — e.g. revealing a live negotiating position. FALSE where the material is already public, obvious from released parts, or basic biography of public figures; speculative or asserted-but-unevidenced harm is insufficient | quote: would, or would be likely to, prejudice the commercial interests of any person | uri: examples/foia/sources/foia_2000.md#L94-L96

atom IntendedFuturePublication: when the request was made, the authority (or someone else) already held the disputed information with a view to publishing it at some future date — whether or not a date was set — and in all the circumstances it is reasonable to withhold it until that publication. FALSE if the intention to publish arose only after the request, or no genuine publication plan exists | quote: held by the public authority with a view to its publication ... at some future date (whether determined or not) | uri: examples/foia/sources/foia_2000.md#L138-L144
atom OngoingResearchProgramme: the disputed information was obtained in the course of, or derives from, a programme of research that is still continuing with a view to publishing a report, and disclosing it before publication would be likely to prejudice the programme, its participants, or the authority holding it | quote: a programme of research ... continuing with a view to the publication | uri: examples/foia/sources/foia_2000.md#L146-L151
atom SecurityBodyInfo: the disputed information was directly or indirectly supplied by, or relates to, one of the national security bodies (the Security Service, the Secret Intelligence Service, GCHQ, the special forces, the security tribunals, the National Crime Agency and related bodies). The connection to such a body is enough — no harm test applies | quote: directly or indirectly supplied to the public authority by, or relates to | uri: examples/foia/sources/foia_2000.md#L153-L159
atom ConfirmWouldRevealSecurityBodyInfo: merely confirming or denying that the information is held would itself reveal something supplied by or relating to those national security bodies | quote: s23(5) excludes the duty to confirm or deny | uri: examples/foia/sources/foia_2000.md#L153-L159
atom SafeguardNationalSecurity: withholding the disputed information is required — reasonably necessary, not merely convenient — for the purpose of safeguarding national security | quote: required for the purpose of safeguarding national security | uri: examples/foia/sources/foia_2000.md#L161-L166
atom NcndRequiredNationalSecurity: refusing even to confirm or deny that the information is held is itself required for the purpose of safeguarding national security | quote: s24(2) excludes the duty to confirm or deny if required for that purpose | uri: examples/foia/sources/foia_2000.md#L161-L166
atom PrejudiceDefence: disclosure of the disputed information would, or would be likely to, prejudice the defence of the British Islands or any colony, or the capability, effectiveness or security of the armed forces. TRUE only on a shown causative link to prejudice that is real and of substance; FALSE on bare assertion | quote: prejudice (a) the defence of the British Islands | uri: examples/foia/sources/foia_2000.md#L168-L172
atom PrejudiceInternationalRelations: disclosure of the disputed information would, or would be likely to, prejudice relations between the United Kingdom and another state, an international organisation or court, or the United Kingdom's interests abroad — or the information is confidential information obtained from another state or international organisation or court | quote: prejudice (a) relations between the United Kingdom and any other State | uri: examples/foia/sources/foia_2000.md#L174-L180
atom PrejudiceUkRelations: disclosure of the disputed information would, or would be likely to, prejudice relations between any two administrations within the United Kingdom (the UK government, the Scottish Ministers, the Welsh government, the Northern Ireland executive) | quote: prejudice relations between any administration in the United Kingdom and any other such administration | uri: examples/foia/sources/foia_2000.md#L182-L186
atom PrejudiceEconomy: disclosure of the disputed information would, or would be likely to, prejudice the economic interests of the United Kingdom or part of it, or the financial interests of a UK administration | quote: prejudice (a) the economic interests of the United Kingdom | uri: examples/foia/sources/foia_2000.md#L188-L192
atom CriminalInvestigationInfo: the disputed information has at any time been held for the purposes of a criminal investigation the authority has a duty to conduct (towards deciding whether someone should be charged), for criminal proceedings the authority conducts, or it relates to the obtaining of information from confidential sources for such purposes. The class matters, not harm: TRUE even if the investigation is closed | quote: any investigation which the public authority has a duty to conduct | uri: examples/foia/sources/foia_2000.md#L194-L200
atom ConfirmWouldRevealInvestigationInfo: merely confirming or denying that such investigation or proceedings information is held would itself reveal something about the investigation, the proceedings, or the confidential sources | quote: s30(3) excludes the duty to confirm or deny | uri: examples/foia/sources/foia_2000.md#L194-L200
atom CourtRecordInfo: the authority holds the disputed information ONLY because it is contained in a document filed with or placed in the custody of a court, served in proceedings, or created by a court or its staff for proceedings (likewise for statutory inquiries and arbitrations). FALSE if the authority also holds it for its own purposes outside the litigation file | quote: held ... only by virtue of being contained in (a) any document filed with | uri: examples/foia/sources/foia_2000.md#L202-L207
atom PrejudiceAuditFunctions: the authority has functions of auditing other public authorities' accounts or examining their economy, efficiency and effectiveness, and disclosure of the disputed information would, or would be likely to, prejudice the exercise of those audit functions | quote: prejudice the exercise of any of the authority's functions | uri: examples/foia/sources/foia_2000.md#L209-L215
atom ParliamentaryPrivilege: withholding the disputed information is required to avoid infringing the privileges of the House of Commons or the House of Lords (their exclusive cognisance over their own proceedings) | quote: required for the purpose of avoiding an infringement of the privileges of either House | uri: examples/foia/sources/foia_2000.md#L217-L220
atom GovernmentPolicyInfo: the disputed information is held by a government department (or the Welsh government) and relates to the formulation or development of government policy, communications between Ministers, the provision of advice by the government's Law Officers, or the operation of a Ministerial private office. The class matters, not harm — but information no longer bearing on live policy weighs less in the public-interest balance | quote: relates to (a) the formulation or development of government policy | uri: examples/foia/sources/foia_2000.md#L222-L227
atom QualifiedPersonOpinionPrejudice: a qualified person (a minister or other statutorily designated senior officer) has given a reasonable opinion that disclosure of the disputed information would, or would be likely to, prejudice collective ministerial responsibility, inhibit the free and frank provision of advice or exchange of views for deliberation, or otherwise prejudice the effective conduct of public affairs. Requires BOTH the opinion to exist AND it to be a reasonable one | quote: in the reasonable opinion of a qualified person | uri: examples/foia/sources/foia_2000.md#L229-L237
atom RoyalSovereignCommunications: the disputed information relates to communications with the Sovereign, with the heir to the Throne, or with the person second in line to the Throne (or with people acting on their behalf) | quote: communications with the Sovereign, (aa) communications with the heir | uri: examples/foia/sources/foia_2000.md#L239-L245
atom RoyalOtherOrHonours: the disputed information relates to communications with members of the Royal Family or Royal Household other than the Sovereign, heir, and second in line — or relates to the conferring by the Crown of any honour or dignity | quote: communications with other members of the Royal Family or Household | uri: examples/foia/sources/foia_2000.md#L239-L245
atom EndangerHealthSafety: disclosure of the disputed information would, or would be likely to, endanger the physical or mental health, or the safety, of any individual. TRUE only on a shown causative link to real endangerment of identifiable people; FALSE on bare assertion | quote: endanger the physical or mental health of any individual | uri: examples/foia/sources/foia_2000.md#L247-L251
atom EnvironmentalInfo: the disputed information is environmental information — about the state of air, water, land, ecosystems, emissions, or measures and activities affecting them — which the authority must handle under the separate environmental information regime instead (or would have to but for one of that regime's own exceptions) | quote: obliged by environmental information regulations to make the information available | uri: examples/foia/sources/foia_2000.md#L253-L258
atom ActionableBreachConfidence: the disputed information was obtained by the authority FROM ANOTHER PERSON, and disclosing it to the public would constitute a breach of confidence on which that person (or someone else) could successfully sue — the information has the necessary quality of confidence, was imparted in circumstances importing an obligation of confidence, disclosure would be unauthorised and detrimental, and no public-interest defence to the breach claim would succeed. FALSE for information the authority generated itself | quote: obtained by the public authority from any other person | uri: examples/foia/sources/foia_2000.md#L260-L266
atom StatutoryProhibition: disclosing the disputed information other than under this access regime is prohibited by or under another enactment, is incompatible with an assimilated (retained EU) obligation, or would constitute or be punishable as a contempt of court | quote: prohibited by or under any enactment | uri: examples/foia/sources/foia_2000.md#L268-L271

# Part I duty blockers (the duty never arises — defeaters, not prohibitions).
atom CostExceedsLimit: the authority estimates that locating, retrieving and extracting the requested information would cost more than the statutory appropriate limit (a fixed money cap on staff time; the estimate must be reasonable and evidence-based) | quote: the cost of complying with the request would exceed the appropriate limit | uri: examples/foia/sources/foia_2000.md#L117-L121
atom VexatiousRequest: the request is vexatious — judged objectively, it imposes a burden, harassment or distress on the authority that is disproportionate to any value or serious purpose the request has. The REQUEST is vexatious, not the requester; a well-founded request does not become vexatious through persistence alone | quote: not oblige a public authority to comply ... if the request is vexatious | uri: examples/foia/sources/foia_2000.md#L123-L126
atom RepeatedRequest: the same person previously made an identical or substantially similar request which the authority complied with, and no reasonable interval has elapsed since | quote: a subsequent identical or substantially similar request | uri: examples/foia/sources/foia_2000.md#L128-L130
atom FeesNoticeUnpaid: the authority gave the applicant a written fees notice for complying with the request and the fee was not paid within three months | quote: not obliged to comply with section 1(1) unless the fee is paid | uri: examples/foia/sources/foia_2000.md#L102-L110

# Administrative duties (s10, s16) — conclusions, not grounding atoms.
atom RespondInTime: the authority responds to the request promptly and at the latest by the twentieth working day after receipt | quote: promptly and in any event not later than the twentieth working day | uri: examples/foia/sources/foia_2000.md#L112-L115
atom AdviseAssist: the authority provides the applicant such advice and assistance with making or pursuing the request as it is reasonable to expect | quote: duty of a public authority to provide advice and assistance | uri: examples/foia/sources/foia_2000.md#L132-L136

# The two public-interest balances (s2(2)(b) for disclosure, s2(1)(b) for NCND).
atom PiMaintainOutweighs: in all the circumstances AT THE TIME OF THE AUTHORITY'S RESPONSE, the public interest in maintaining the engaged qualified exemption outweighs the public interest in disclosing the disputed information. Weigh the ACTUAL harm this disclosure risks against the ACTUAL benefit of disclosing THIS material: a generic transparency interest weighs little if the specific material sheds little light on the matter of public debate. Where the engaged exemption is legal professional privilege, the inherent interest in keeping legal advice confidential is very strong and only exceptional countervailing factors displace it. Only meaningful when some qualified exemption is engaged | quote: the public interest in maintaining the exemption outweighs the public interest in disclosing | uri: examples/foia/sources/foia_2000.md#L29-L33
atom PiNcndMaintainOutweighs: the same balance applied to the duty to confirm or deny: the public interest in not even revealing WHETHER the information is held outweighs the public interest in knowing that. Only meaningful when confirming or denying would itself cause the relevant harm | quote: maintaining the exclusion of the duty to confirm or deny outweighs | uri: examples/foia/sources/foia_2000.md#L23-L27

# ---------------------------------------------------------------------------
# s1 duties — borne by the public authority; s10/s16 administrative duties
# ---------------------------------------------------------------------------
duty_confirm:  Request  =>O@Authority  ConfirmOrDeny
duty_disclose: Request, HoldsInfo  =>O@Authority  Disclose
duty_timely:   Request  =>O@Authority  RespondInTime
duty_advise:   Request  =>O@Authority  AdviseAssist

# ---------------------------------------------------------------------------
# Part I duty blockers (s9, s12, s14) — defeaters: the s1 duty never arises,
# the act is merely not-obligated (P), not forbidden (F)
# ---------------------------------------------------------------------------
s12_cost:     CostExceedsLimit  ~>O@Authority  ~Disclose
s14_vex:      VexatiousRequest  ~>O@Authority  ~Disclose
s14_vex_ncnd: VexatiousRequest  ~>O@Authority  ~ConfirmOrDeny
s14_rep:      RepeatedRequest  ~>O@Authority  ~Disclose
s9_fees:      FeesNoticeUnpaid  ~>O@Authority  ~Disclose
s9_fees_ncnd: FeesNoticeUnpaid  ~>O@Authority  ~ConfirmOrDeny

# ---------------------------------------------------------------------------
# Absolute exemptions (s2(3)) — engagement alone defeats the duty
# ---------------------------------------------------------------------------
s21_exempt:   AccessibleOtherMeans  =>O@Authority  ~Disclose
s23_exempt:   SecurityBodyInfo  =>O@Authority  ~Disclose
s32_exempt:   CourtRecordInfo  =>O@Authority  ~Disclose
s34_exempt:   ParliamentaryPrivilege  =>O@Authority  ~Disclose
s37_royal_exempt: RoyalSovereignCommunications  =>O@Authority  ~Disclose
s40_1_exempt: ApplicantOwnData  =>O@Authority  ~Disclose
s40_2_exempt: ThirdPartyPersonalData, ContraveneDPPrinciples  =>O@Authority  ~Disclose
s41_exempt:   ActionableBreachConfidence  =>O@Authority  ~Disclose
s44_exempt:   StatutoryProhibition  =>O@Authority  ~Disclose

# ---------------------------------------------------------------------------
# Qualified exemptions — engagement AND the s2(2)(b) balance
# ---------------------------------------------------------------------------
s22_exempt:   IntendedFuturePublication, PiMaintainOutweighs  =>O@Authority  ~Disclose
s22a_exempt:  OngoingResearchProgramme, PiMaintainOutweighs  =>O@Authority  ~Disclose
s24_exempt:   SafeguardNationalSecurity, PiMaintainOutweighs  =>O@Authority  ~Disclose
s26_exempt:   PrejudiceDefence, PiMaintainOutweighs  =>O@Authority  ~Disclose
s27_exempt:   PrejudiceInternationalRelations, PiMaintainOutweighs  =>O@Authority  ~Disclose
s28_exempt:   PrejudiceUkRelations, PiMaintainOutweighs  =>O@Authority  ~Disclose
s29_exempt:   PrejudiceEconomy, PiMaintainOutweighs  =>O@Authority  ~Disclose
s30_exempt:   CriminalInvestigationInfo, PiMaintainOutweighs  =>O@Authority  ~Disclose
s31_exempt:   PrejudiceLawEnforcement, PiMaintainOutweighs  =>O@Authority  ~Disclose
s33_exempt:   PrejudiceAuditFunctions, PiMaintainOutweighs  =>O@Authority  ~Disclose
s35_exempt:   GovernmentPolicyInfo, PiMaintainOutweighs  =>O@Authority  ~Disclose
s36_exempt:   QualifiedPersonOpinionPrejudice, PiMaintainOutweighs  =>O@Authority  ~Disclose
s37_other_exempt: RoyalOtherOrHonours, PiMaintainOutweighs  =>O@Authority  ~Disclose
s38_exempt:   EndangerHealthSafety, PiMaintainOutweighs  =>O@Authority  ~Disclose
s39_exempt:   EnvironmentalInfo, PiMaintainOutweighs  =>O@Authority  ~Disclose
s42_exempt:   LegalPrivilege, PiMaintainOutweighs  =>O@Authority  ~Disclose
s43_1_exempt: TradeSecret, PiMaintainOutweighs  =>O@Authority  ~Disclose
s43_2_exempt: PrejudiceCommercialInterests, PiMaintainOutweighs  =>O@Authority  ~Disclose

# ---------------------------------------------------------------------------
# NCND — exclusions of the duty to confirm or deny, stacking on an exemption
# ---------------------------------------------------------------------------
s23_ncnd:    ConfirmWouldRevealSecurityBodyInfo  =>O@Authority  ~ConfirmOrDeny
s24_ncnd:    NcndRequiredNationalSecurity, PiNcndMaintainOutweighs  =>O@Authority  ~ConfirmOrDeny
s30_ncnd:    ConfirmWouldRevealInvestigationInfo, PiNcndMaintainOutweighs  =>O@Authority  ~ConfirmOrDeny
s40_5a_ncnd: ApplicantOwnData  =>O@Authority  ~ConfirmOrDeny
s31_3_ncnd:  ConfirmPrejudiceLawEnforcement, PiNcndMaintainOutweighs  =>O@Authority  ~ConfirmOrDeny

# ---------------------------------------------------------------------------
# s17 — withholding under an exemption triggers the refusal-notice duty
# (deontic body literal: fires only once ~Disclose is actually obligatory)
# ---------------------------------------------------------------------------
s17_notice: Request, O(~Disclose)  =>O@Authority  RefusalNotice

# ---------------------------------------------------------------------------
# s2 superiority — an engaged exemption defeats the s1 duty; NCND exclusions
# defeat the duty to confirm or deny; Part I blockers defeat both.
# ---------------------------------------------------------------------------
superiority: s21_exempt > duty_disclose, s23_exempt > duty_disclose, s32_exempt > duty_disclose, s34_exempt > duty_disclose, s37_royal_exempt > duty_disclose, s40_1_exempt > duty_disclose, s40_2_exempt > duty_disclose, s41_exempt > duty_disclose, s44_exempt > duty_disclose, s22_exempt > duty_disclose, s22a_exempt > duty_disclose, s24_exempt > duty_disclose, s26_exempt > duty_disclose, s27_exempt > duty_disclose, s28_exempt > duty_disclose, s29_exempt > duty_disclose, s30_exempt > duty_disclose, s31_exempt > duty_disclose, s33_exempt > duty_disclose, s35_exempt > duty_disclose, s36_exempt > duty_disclose, s37_other_exempt > duty_disclose, s38_exempt > duty_disclose, s39_exempt > duty_disclose, s42_exempt > duty_disclose, s43_1_exempt > duty_disclose, s43_2_exempt > duty_disclose, s23_ncnd > duty_confirm, s24_ncnd > duty_confirm, s30_ncnd > duty_confirm, s40_5a_ncnd > duty_confirm, s31_3_ncnd > duty_confirm, s12_cost > duty_disclose, s14_vex > duty_disclose, s14_vex_ncnd > duty_confirm, s14_rep > duty_disclose, s9_fees > duty_disclose, s9_fees_ncnd > duty_confirm

# ---------------------------------------------------------------------------
# CLI smoke checks (see also tests.sh):
#   deontic query examples/foia/foia.ddl Disclose RefusalNotice \
#       --assume Request,HoldsInfo,ThirdPartyPersonalData,ContraveneDPPrinciples
#     → F(Disclose) · O(RefusalNotice)                       [s40(2) upheld]
#   deontic query examples/foia/foia.ddl Disclose \
#       --assume Request,HoldsInfo,PrejudiceCommercialInterests
#     → O(Disclose)                       [s43 engaged but PI favours disclosure]
#   deontic abduce examples/foia/foia.ddl 'O@Authority(~Disclose)' --all
#     → the minimal withholding configurations (one per exemption path)
# ---------------------------------------------------------------------------
