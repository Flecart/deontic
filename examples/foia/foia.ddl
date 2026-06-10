# Freedom of Information Act 2000 — pilot formalization (Parts I–II slice)
# ---------------------------------------------------------------------------
# Scope: the s1 access duties, the s2 absolute/qualified exemption layer, the
# s17 refusal notice, NCND, and five exemptions (s21, s31, s40, s42, s43) —
# the pilot subset of docs/experiments/foia_corpus/INDEX.md.
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

# The two public-interest balances (s2(2)(b) for disclosure, s2(1)(b) for NCND).
atom PiMaintainOutweighs: in all the circumstances AT THE TIME OF THE AUTHORITY'S RESPONSE, the public interest in maintaining the engaged qualified exemption outweighs the public interest in disclosing the disputed information. Weigh the ACTUAL harm this disclosure risks against the ACTUAL benefit of disclosing THIS material: a generic transparency interest weighs little if the specific material sheds little light on the matter of public debate. Where the engaged exemption is legal professional privilege, the inherent interest in keeping legal advice confidential is very strong and only exceptional countervailing factors displace it. Only meaningful when some qualified exemption is engaged | quote: the public interest in maintaining the exemption outweighs the public interest in disclosing | uri: examples/foia/sources/foia_2000.md#L29-L33
atom PiNcndMaintainOutweighs: the same balance applied to the duty to confirm or deny: the public interest in not even revealing WHETHER the information is held outweighs the public interest in knowing that. Only meaningful when confirming or denying would itself cause the relevant harm | quote: maintaining the exclusion of the duty to confirm or deny outweighs | uri: examples/foia/sources/foia_2000.md#L23-L27

# ---------------------------------------------------------------------------
# s1 duties — borne by the public authority
# ---------------------------------------------------------------------------
duty_confirm:  Request  =>O@Authority  ConfirmOrDeny
duty_disclose: Request, HoldsInfo  =>O@Authority  Disclose

# ---------------------------------------------------------------------------
# Absolute exemptions (s2(3)) — engagement alone defeats the duty
# ---------------------------------------------------------------------------
s21_exempt:   AccessibleOtherMeans  =>O@Authority  ~Disclose
s40_1_exempt: ApplicantOwnData  =>O@Authority  ~Disclose
s40_2_exempt: ThirdPartyPersonalData, ContraveneDPPrinciples  =>O@Authority  ~Disclose

# ---------------------------------------------------------------------------
# Qualified exemptions — engagement AND the s2(2)(b) balance
# ---------------------------------------------------------------------------
s31_exempt:   PrejudiceLawEnforcement, PiMaintainOutweighs  =>O@Authority  ~Disclose
s42_exempt:   LegalPrivilege, PiMaintainOutweighs  =>O@Authority  ~Disclose
s43_1_exempt: TradeSecret, PiMaintainOutweighs  =>O@Authority  ~Disclose
s43_2_exempt: PrejudiceCommercialInterests, PiMaintainOutweighs  =>O@Authority  ~Disclose

# ---------------------------------------------------------------------------
# NCND — exclusions of the duty to confirm or deny, stacking on an exemption
# ---------------------------------------------------------------------------
s40_5a_ncnd: ApplicantOwnData  =>O@Authority  ~ConfirmOrDeny
s31_3_ncnd:  ConfirmPrejudiceLawEnforcement, PiNcndMaintainOutweighs  =>O@Authority  ~ConfirmOrDeny

# ---------------------------------------------------------------------------
# s17 — withholding under an exemption triggers the refusal-notice duty
# (deontic body literal: fires only once ~Disclose is actually obligatory)
# ---------------------------------------------------------------------------
s17_notice: Request, O(~Disclose)  =>O@Authority  RefusalNotice

# ---------------------------------------------------------------------------
# s2 superiority — an engaged exemption defeats the s1 duty; NCND exclusions
# defeat the duty to confirm or deny.
# ---------------------------------------------------------------------------
superiority: s21_exempt > duty_disclose, s40_1_exempt > duty_disclose, s40_2_exempt > duty_disclose, s31_exempt > duty_disclose, s42_exempt > duty_disclose, s43_1_exempt > duty_disclose, s43_2_exempt > duty_disclose, s40_5a_ncnd > duty_confirm, s31_3_ncnd > duty_confirm

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
