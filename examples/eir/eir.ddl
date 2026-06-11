# Environmental Information Regulations 2004 — formalization
# ---------------------------------------------------------------------------
# Domain #2 of the formalization dataset (after FOIA — see
# docs/experiments/DOMAINS.md). Structural differences from FOIA, modelled
# deliberately:
#   * EVERY exception is qualified (reg 12(1)(b) public-interest test); the
#     only near-absolute path is reg 13 first-condition personal data.
#   * Reg 12(2) PRESUMPTION in favour of disclosure: in equipoise the
#     requester wins — baked into the PiMaintainOutweighs truth conditions.
#   * Reg 12(5) uses "would adversely affect" — a HIGHER bar than FOIA's
#     "would be likely to prejudice" (must be more probable than not).
#   * Reg 12(4)(a) (not held) is not a rule: it is the absence of HoldsInfo,
#     which leaves the duty inapplicable (status P, mapped to refusal upheld).
# Shared contracts: ThirdPartyPersonalData and ContraveneDPPrinciples carry
# the same descriptions as in examples/foia/foia.ddl (same legal test), so a
# guarded merge of the two theories stays legal.
facts:

# ---------------------------------------------------------------------------
# Core atoms
# ---------------------------------------------------------------------------
atom Request: a person has made a request to the public authority for information (any form; environmental requests need not cite any statute). TRUE whenever the case shows a request was made; procedural, but assert it when it holds | quote: shall make it available on request | uri: examples/eir/sources/eir_2004.md#L22-L26
atom IsEnvironmentalInfo: the requested information is environmental information — it is on the state of the elements of the environment (air, atmosphere, water, soil, land, landscape, natural sites); on factors affecting them (substances, energy, noise, radiation, waste, emissions); on measures or activities affecting or likely to affect them or designed to protect them (policies, legislation, plans, programmes, agreements); on reports on implementing environmental legislation; on economic analyses used within such measures; or on the state of human health and safety as affected by the environment. Construe broadly | quote: the state of the elements of the environment | uri: examples/eir/sources/eir_2004.md#L8-L20
atom HoldsInfo: the authority held the requested environmental information when the request was received, judged for the DISPUTED information. TRUE if it exists and is held, even though withheld; FALSE if not held when the request arrived | quote: it does not hold that information when an applicant's request is received | uri: examples/eir/sources/eir_2004.md#L38-L45
atom Disclose: the authority makes the disputed environmental information available to the applicant. The decision atom — never assert it as a fact | quote: shall make it available on request | uri: examples/eir/sources/eir_2004.md#L22-L26
atom RefusalNotice: the authority gave the applicant a written refusal specifying which exception it relies on and why. TRUE whenever the refusal cited an exception — assert it even though procedural | quote: may refuse to disclose environmental information | uri: examples/eir/sources/eir_2004.md#L28-L33

# ---------------------------------------------------------------------------
# Class exceptions (reg 12(4)(b)-(e)) — grounding atoms
# ---------------------------------------------------------------------------
atom ManifestlyUnreasonable: the request is manifestly unreasonable — judged objectively, it imposes a burden or harassment on the authority clearly disproportionate to any value or serious purpose it has (the environmental analogue of a vexatious or excessively costly request) | quote: the request for information is manifestly unreasonable | uri: examples/eir/sources/eir_2004.md#L38-L45
atom TooGeneralRequest: the request is formulated in too general a manner for the authority to identify what is sought, AND the authority has already asked the applicant to particularise it and offered advice and assistance. FALSE if the request, read fairly, identifies the information | quote: formulated in too general a manner | uri: examples/eir/sources/eir_2004.md#L38-L45
atom MaterialInCourseOfCompletion: the disputed information relates to material still in the course of completion, to unfinished documents, or to incomplete data — work actively still being drafted or compiled at the time of the request. FALSE for finished documents that merely feed a continuing wider process | quote: material which is still in the course of completion | uri: examples/eir/sources/eir_2004.md#L38-L45
atom InternalCommunications: disclosing the disputed information would involve disclosing communications internal to a public authority (including between a government department's officials or with its ministers); communications WITH external parties are not internal | quote: involves the disclosure of internal communications | uri: examples/eir/sources/eir_2004.md#L38-L45

# ---------------------------------------------------------------------------
# Adverse-effect exceptions (reg 12(5)) — "would adversely affect" requires
# that harm is MORE PROBABLE THAN NOT, a higher bar than likelihood
# ---------------------------------------------------------------------------
atom AdverseIntlSecurity: disclosure of the disputed information would (more probably than not) adversely affect international relations, defence, national security or public safety. FALSE on bare assertion or mere risk | quote: international relations, defence, national security or public safety | uri: examples/eir/sources/eir_2004.md#L47-L57
atom AdverseCourseOfJustice: disclosure would (more probably than not) adversely affect the course of justice, a person's ability to receive a fair trial, or an authority's ability to conduct a criminal or disciplinary inquiry — includes material covered by legal professional privilege while litigation or advice interests persist | quote: the course of justice, the ability of a person to receive a fair trial | uri: examples/eir/sources/eir_2004.md#L47-L57
atom AdverseIntellectualProperty: disclosure would (more probably than not) adversely affect intellectual property rights — the rights-holder's ability to exploit copyright, database right or patent in the material would actually be harmed, not merely engaged | quote: intellectual property rights | uri: examples/eir/sources/eir_2004.md#L47-L57
atom AdverseProceedingsConfidentiality: disclosure would (more probably than not) adversely affect the confidentiality of an authority's proceedings, where that confidentiality is provided by law — formal deliberative proceedings whose confidentiality a statute or common-law duty protects | quote: the confidentiality of the proceedings of that or any other public authority | uri: examples/eir/sources/eir_2004.md#L47-L57
atom AdverseCommercialConfidentiality: disclosure would (more probably than not) adversely affect the confidentiality of commercial or industrial information, where that confidentiality is provided by law (a duty of confidence or statutory protection) and protects a legitimate economic interest | quote: the confidentiality of commercial or industrial information | uri: examples/eir/sources/eir_2004.md#L47-L57
atom AdverseVolunteerInterests: the disputed information was supplied voluntarily by a person who was not under (and could not be put under) a legal obligation to supply it, who has not consented to disclosure, and disclosure would (more probably than not) adversely affect that person's interests | quote: the interests of the person who provided the information | uri: examples/eir/sources/eir_2004.md#L47-L57
atom AdverseEnvironmentProtection: disclosure would (more probably than not) adversely affect the protection of the very environment the information relates to — e.g. revealing the location of rare species or vulnerable sites | quote: the protection of the environment to which the information relates | uri: examples/eir/sources/eir_2004.md#L47-L57

# ---------------------------------------------------------------------------
# Reg 13 personal data — same contracts as the FOIA theory (same legal test)
# ---------------------------------------------------------------------------
atom ThirdPartyPersonalData: the disputed information constitutes personal data of identifiable living individuals other than the applicant — it relates to them and is biographical in a significant sense. TRUE even for senior officials or public figures; their seniority affects the separate question whether disclosure would contravene the data-protection principles (the ContraveneDPPrinciples atom), not this one | quote: a public authority must not disclose the personal data | uri: examples/eir/sources/eir_2004.md#L59-L66
atom ContraveneDPPrinciples: disclosing the third-party personal data to a member of the public would contravene a data-protection principle — chiefly the requirement that processing be lawful and fair: public disclosure of personal data is lawful only when it is necessary for a legitimate interest pursued by the requester or the public, and that interest is not overridden by the data subjects' own interests, rights and freedoms. Apply three steps: (i) is there a legitimate interest in disclosure; (ii) is disclosing THIS material NECESSARY for that interest — necessity fails (and this atom is TRUE) if a less intrusive means, such as an already-published summary, already serves the interest; (iii) if necessary, do the data subjects' rights and reasonable expectations override the interest. FALSE where the legitimate interest genuinely requires this very material and outweighs the subjects' rights (e.g. data the subjects already made public themselves) | quote: the first condition is satisfied | uri: examples/eir/sources/eir_2004.md#L59-L66

# The reg 12(1)(b) balance, shaped by the reg 12(2) presumption.
atom PiMaintainOutweighs: in all the circumstances at the time of the authority's response, the public interest in maintaining the engaged exception OUTWEIGHS the public interest in disclosing the disputed information. The presumption in favour of disclosure applies: if the competing interests are evenly balanced, this atom is FALSE and the information must be disclosed. Weigh the actual harm of THIS disclosure against the actual benefit of THIS material | quote: A public authority shall apply a presumption in favour of disclosure | uri: examples/eir/sources/eir_2004.md#L28-L36

# ---------------------------------------------------------------------------
# Reg 5(1) duty; reg 14 refusal notice
# ---------------------------------------------------------------------------
duty_disclose: Request, IsEnvironmentalInfo, HoldsInfo  =>O@Authority  Disclose
reg14_notice:  Request, O(~Disclose)  =>O@Authority  RefusalNotice

# ---------------------------------------------------------------------------
# Exceptions — every one qualified by the PI balance (reg 12(1)(b));
# reg 13 first condition stands alone (no balance once DP contravened)
# ---------------------------------------------------------------------------
r12_4b_exc: ManifestlyUnreasonable, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_4c_exc: TooGeneralRequest, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_4d_exc: MaterialInCourseOfCompletion, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_4e_exc: InternalCommunications, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_5a_exc: AdverseIntlSecurity, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_5b_exc: AdverseCourseOfJustice, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_5c_exc: AdverseIntellectualProperty, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_5d_exc: AdverseProceedingsConfidentiality, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_5e_exc: AdverseCommercialConfidentiality, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_5f_exc: AdverseVolunteerInterests, PiMaintainOutweighs  =>O@Authority  ~Disclose
r12_5g_exc: AdverseEnvironmentProtection, PiMaintainOutweighs  =>O@Authority  ~Disclose
r13_exc:    ThirdPartyPersonalData, ContraveneDPPrinciples  =>O@Authority  ~Disclose

superiority: r12_4b_exc > duty_disclose, r12_4c_exc > duty_disclose, r12_4d_exc > duty_disclose, r12_4e_exc > duty_disclose, r12_5a_exc > duty_disclose, r12_5b_exc > duty_disclose, r12_5c_exc > duty_disclose, r12_5d_exc > duty_disclose, r12_5e_exc > duty_disclose, r12_5f_exc > duty_disclose, r12_5g_exc > duty_disclose, r13_exc > duty_disclose
