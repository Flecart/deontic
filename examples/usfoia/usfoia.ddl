# 5 U.S.C. § 552 (US FOIA) — formalization (domain #5 of the dataset)
# ---------------------------------------------------------------------------
# The cross-jurisdiction replication of the UK FOIA flagship. Structural
# differences modelled deliberately:
#   * No UK-style public-interest balance. Instead the (a)(8)(A) FORESEEABLE
#     HARM standard: an exemption (other than a (b)(3) statutory bar or
#     properly classified (b)(1) material) only sustains withholding if the
#     agency reasonably foresees that disclosure would harm the interest the
#     exemption protects — modelled as the ForeseeableHarm atom conjoined to
#     the discretionary exemptions.
#   * Segregability is a per-portion duty: like UK part-splits, each disputed
#     segregable portion is its own case instance.
# Decision atom: Disclose, borne by @Agency. Gold: disclose / withhold.
facts:

atom Request: a person made a request that reasonably describes the records sought and complies with the agency's published procedures. TRUE for virtually every litigated case; procedural, but assert it when it holds | quote: shall make the records promptly available to any person | uri: examples/usfoia/sources/usc552.md#L6-L10
atom HoldsRecords: the agency has the requested records, judged for the DISPUTED portions. TRUE if they exist and are held, even though withheld; FALSE if no responsive records exist after an adequate search | quote: shall make the records promptly available | uri: examples/usfoia/sources/usc552.md#L6-L10
atom Disclose: the agency releases the disputed records (or portions) to the requester. The decision atom — never assert it as a fact | quote: shall make the records promptly available | uri: examples/usfoia/sources/usc552.md#L6-L10
atom ForeseeableHarm: the agency reasonably foresees that disclosing the disputed material would harm an interest protected by the exemption it claims — a specific, articulable harm from THIS disclosure, not a generic invocation of the exemption's category. FALSE where the agency offered only boilerplate or category-level justification | quote: reasonably foresees that disclosure would harm an interest protected by an exemption | uri: examples/usfoia/sources/usc552.md#L12-L17

# Exemption-engagement atoms (the (b) categories' own tests)
atom ProperlyClassified: the disputed material is in fact properly classified under the criteria of an Executive order in the interest of national defense or foreign policy — both procedurally and substantively | quote: properly classified under an Executive order | uri: examples/usfoia/sources/usc552.md#L19-L37
atom InternalPersonnelRules: the disputed material relates solely to the internal personnel rules and practices of the agency — trivial internal housekeeping with no genuine public interest | quote: related solely to internal personnel rules and practices | uri: examples/usfoia/sources/usc552.md#L19-L37
atom StatutoryBar: another statute specifically exempts the disputed material from disclosure, leaving no agency discretion or establishing particular withholding criteria | quote: specifically exempted from disclosure by another statute | uri: examples/usfoia/sources/usc552.md#L19-L37
atom ConfidentialCommercial: the disputed material is a trade secret, or commercial or financial information obtained from a person outside government that is privileged or customarily and actually treated as confidential by its owner | quote: trade secrets and commercial or financial information | uri: examples/usfoia/sources/usc552.md#L19-L37
atom DeliberativePrivileged: the disputed material is an inter-agency or intra-agency communication that would be privileged against discovery in litigation — pre-decisional and deliberative (the deliberative-process privilege), attorney-client advice, or attorney work product | quote: inter-agency or intra-agency memorandums or letters | uri: examples/usfoia/sources/usc552.md#L19-L37
atom UnwarrantedPrivacyInvasion: the disputed material is in personnel, medical or similar files and disclosing it would constitute a clearly unwarranted invasion of personal privacy — the individuals' privacy interest outweighs the public interest in what the disclosure would reveal about government conduct | quote: clearly unwarranted invasion of personal privacy | uri: examples/usfoia/sources/usc552.md#L19-L37
atom LawEnforcementHarm: the disputed records were compiled for law enforcement purposes AND disclosure could reasonably be expected to cause one of the enumerated harms — interfering with enforcement proceedings, unwarranted invasion of personal privacy, exposing a confidential source, revealing investigative techniques whose disclosure would risk circumvention of the law, or endangering someone's life or physical safety | quote: records or information compiled for law enforcement purposes | uri: examples/usfoia/sources/usc552.md#L19-L37
atom FinancialExamination: the disputed material is contained in or related to examination or condition reports about financial institutions prepared for their regulators | quote: examination reports of agencies regulating financial institutions | uri: examples/usfoia/sources/usc552.md#L19-L37
atom WellData: the disputed material is geological or geophysical information or data concerning wells | quote: geological and geophysical information and data concerning wells | uri: examples/usfoia/sources/usc552.md#L19-L37

# ---------------------------------------------------------------------------
# The (a)(3) duty
# ---------------------------------------------------------------------------
duty_disclose: Request, HoldsRecords  =>O@Agency  Disclose

# ---------------------------------------------------------------------------
# Mandatory bars: no foreseeable-harm showing needed
# ---------------------------------------------------------------------------
b1_exempt: ProperlyClassified  =>O@Agency  ~Disclose
b3_exempt: StatutoryBar  =>O@Agency  ~Disclose

# ---------------------------------------------------------------------------
# Discretionary exemptions: engagement AND (a)(8)(A) foreseeable harm
# ---------------------------------------------------------------------------
b2_exempt: InternalPersonnelRules, ForeseeableHarm  =>O@Agency  ~Disclose
b4_exempt: ConfidentialCommercial, ForeseeableHarm  =>O@Agency  ~Disclose
b5_exempt: DeliberativePrivileged, ForeseeableHarm  =>O@Agency  ~Disclose
b6_exempt: UnwarrantedPrivacyInvasion, ForeseeableHarm  =>O@Agency  ~Disclose
b7_exempt: LawEnforcementHarm, ForeseeableHarm  =>O@Agency  ~Disclose
b8_exempt: FinancialExamination, ForeseeableHarm  =>O@Agency  ~Disclose
b9_exempt: WellData, ForeseeableHarm  =>O@Agency  ~Disclose

superiority: b1_exempt > duty_disclose, b3_exempt > duty_disclose, b2_exempt > duty_disclose, b4_exempt > duty_disclose, b5_exempt > duty_disclose, b6_exempt > duty_disclose, b7_exempt > duty_disclose, b8_exempt > duty_disclose, b9_exempt > duty_disclose
