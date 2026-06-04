# Enterprise SaaS Master Services Agreement (synthetic composite)
# ---------------------------------------------------------------------------
# A deliberately dense MSA encoding: license scope, fee suspension with cure,
# SLA credits (compensatory), confidentiality carve-outs, DPA/subprocessors,
# security-incident notify→remediate chain, indemnity vs liability-cap interaction,
# termination wind-down, non-solicit exception, insurance, and audit.
#
# Source excerpts: examples/clauses/sources/enterprise_saas_msa.md
#
# Facts are scenario-specific; default empty for abduction. Uncomment one block
# below or pass facts via a derived copy / fact-finder output.
facts:

# --- Scenario A: payment overdue (suspension + compensatory cure) ---
# Vendor has not yet suspended — expect [NON-COMPENSABLE VIOLATION] on SuspendAccess.
# facts: CustomerParty, OrderFormExecuted, PaymentOverdue

# --- Scenario B: SLA miss (service credits as sole remedy) ---
# facts: CustomerParty, OrderFormExecuted, ActiveSla, SlaFailure

# --- Scenario C: employee confidentiality share (awareness gate) ---
# facts: CustomerParty, EmployeeNeedToKnow, EmployeeUnderNDA

# --- Scenario D: IP claim with liability cap (excluded liability wins) ---
# facts: CustomerParty, IpInfringementClaim, ThirdPartyClaim, LiabilityCapApplies, ExcludedLiability

# --- Scenario E: non-solicit exception ---
# facts: CustomerParty, EmployeeInitiatedContact

# ---------------------------------------------------------------------------
# Party / relationship
# ---------------------------------------------------------------------------
atom CustomerParty: Customer is party to the MSA and an executed Order Form | quote: Customer | uri: examples/clauses/sources/enterprise_saas_msa.md#L7-L8
atom OrderFormExecuted: an Order Form has been executed by both parties | quote: Upon execution of an Order Form | uri: examples/clauses/sources/enterprise_saas_msa.md#L7-L8
atom ValidSubscriptionLicense: Vendor has granted Customer a non-exclusive license to use the Software for the Subscription Term | quote: grants Customer a non-exclusive, non-transferable license | uri: examples/clauses/sources/enterprise_saas_msa.md#L7-L10
atom UseSoftware: Customer uses the Software | quote: license to use the Software | uri: examples/clauses/sources/enterprise_saas_msa.md#L8-L9
atom ExceedOrderScope: Customer uses the Software outside the scope stated in the Order Form | quote: shall not exceed the scope of use | uri: examples/clauses/sources/enterprise_saas_msa.md#L9-L10
atom MaterialBreach: an act or omission constitutes a material breach of the Agreement | quote: material breach | uri: examples/clauses/sources/enterprise_saas_msa.md#L10-L11

# ---------------------------------------------------------------------------
# Fees and suspension (compensatory cure chain)
# ---------------------------------------------------------------------------
atom FeesDue: fees are due and payable under the Order Form | quote: shall pay all fees when due | uri: examples/clauses/sources/enterprise_saas_msa.md#L15-L16
atom PayFees: Customer pays all fees when due | quote: shall pay all fees when due | uri: examples/clauses/sources/enterprise_saas_msa.md#L15-L16
atom PaymentOverdue: payment is more than thirty (30) days overdue | quote: more than thirty (30) days overdue | uri: examples/clauses/sources/enterprise_saas_msa.md#L16-L17
atom SuspendAccess: Vendor suspends Customer's access to the Software | quote: may suspend access to the Software | uri: examples/clauses/sources/enterprise_saas_msa.md#L17-L18
atom PayOverdueAmounts: Customer pays all overdue amounts | quote: until Customer pays all overdue amounts | uri: examples/clauses/sources/enterprise_saas_msa.md#L17-L18
atom RestoreAccess: Vendor restores access within two (2) business days after overdue payment | quote: shall restore access within two (2) business days | uri: examples/clauses/sources/enterprise_saas_msa.md#L18-L19

# ---------------------------------------------------------------------------
# Service levels (compensatory credits)
# ---------------------------------------------------------------------------
atom ActiveSla: a service-level agreement is in effect for the Subscription | quote: During an active SLA | uri: examples/clauses/sources/enterprise_saas_msa.md#L23-L24
atom MeetUptimeTarget: Vendor maintains at least 99.9% monthly uptime | quote: maintain monthly uptime of at least 99.9% | uri: examples/clauses/sources/enterprise_saas_msa.md#L24-L25
atom SlaFailure: Vendor failed to meet uptime in a calendar month | quote: fails to meet uptime in a calendar month | uri: examples/clauses/sources/enterprise_saas_msa.md#L25-L26
atom ClaimServiceCredits: Customer claims service credits for the SLA failure | quote: may claim service credits | uri: examples/clauses/sources/enterprise_saas_msa.md#L26-L27

# ---------------------------------------------------------------------------
# Confidentiality
# ---------------------------------------------------------------------------
atom DiscloseConfidentialInfo: a party discloses the other party's Confidential Information to a third person | quote: shall not disclose the other party's Confidential Information | uri: examples/clauses/sources/enterprise_saas_msa.md#L31-L32
atom EmployeeNeedToKnow: the recipient is an employee with a need to know the Confidential Information | quote: employees who have a need to know | uri: examples/clauses/sources/enterprise_saas_msa.md#L32-L33
atom EmployeeUnderNDA: the employee is bound by obligations no less protective than this Agreement | quote: bound by obligations no less protective | uri: examples/clauses/sources/enterprise_saas_msa.md#L33-L34
atom LegalCompulsionRequired: disclosure is required by law or court order | quote: required by law or court order | uri: examples/clauses/sources/enterprise_saas_msa.md#L34-L35

# ---------------------------------------------------------------------------
# Data processing
# ---------------------------------------------------------------------------
atom ProcessPersonalData: Vendor processes Customer Personal Data | quote: process Personal Data | uri: examples/clauses/sources/enterprise_saas_msa.md#L39-L40
atom LawfulDataInstruction: Customer has given documented instructions for the processing | quote: only on documented instructions from Customer | uri: examples/clauses/sources/enterprise_saas_msa.md#L39-L40
atom EngageSubprocessor: Vendor engages a subprocessor to process Personal Data | quote: engage a subprocessor | uri: examples/clauses/sources/enterprise_saas_msa.md#L41-L42
atom SubprocessorNoticeGiven: Vendor gave Customer at least thirty (30) days' prior notice of the subprocessor | quote: thirty (30) days' prior notice | uri: examples/clauses/sources/enterprise_saas_msa.md#L41-L42

# ---------------------------------------------------------------------------
# Security incidents (notify then remediate)
# ---------------------------------------------------------------------------
atom ImplementSecurityMeasures: Vendor implements appropriate technical and organisational security measures | quote: implement appropriate technical and organisational security measures | uri: examples/clauses/sources/enterprise_saas_msa.md#L46-L47
atom SecurityIncident: a Security Incident affecting Customer Personal Data has occurred | quote: Security Incident affecting Customer Personal Data | uri: examples/clauses/sources/enterprise_saas_msa.md#L47-L48
atom NotifyCustomer: Vendor notifies Customer of the Security Incident within seventy-two (72) hours where feasible | quote: notify Customer without undue delay and, where feasible, within seventy-two (72) hours | uri: examples/clauses/sources/enterprise_saas_msa.md#L48-L49
atom RemediateIncident: Vendor takes reasonable steps to remediate the Security Incident | quote: take reasonable steps to remediate the incident | uri: examples/clauses/sources/enterprise_saas_msa.md#L49-L50

# ---------------------------------------------------------------------------
# Indemnity and liability cap
# ---------------------------------------------------------------------------
atom ThirdPartyClaim: a third party brings a claim against Customer | quote: third-party claims | uri: examples/clauses/sources/enterprise_saas_msa.md#L54-L55
atom VendorMaterialBreach: Vendor has materially breached the Agreement | quote: Vendor's breach of the Agreement | uri: examples/clauses/sources/enterprise_saas_msa.md#L54-L55
atom IpInfringementClaim: a third-party claim alleges the Software infringes intellectual property rights | quote: infringement of a third party's intellectual property rights | uri: examples/clauses/sources/enterprise_saas_msa.md#L55-L56
atom IndemnifyCustomer: Vendor indemnifies Customer against the claim | quote: shall indemnify Customer | uri: examples/clauses/sources/enterprise_saas_msa.md#L54-L55
atom LiabilityCapApplies: the claim falls within the general aggregate liability cap (fees paid in the prior twelve months) | quote: aggregate liability ... is capped at the fees paid | uri: examples/clauses/sources/enterprise_saas_msa.md#L56-L57
atom ExcludedLiability: the claim is an Excluded Liability (fraud, wilful misconduct, confidentiality breach, or IP indemnity) | quote: Excluded Liabilities include fraud, wilful misconduct, breach of confidentiality obligations, and intellectual property infringement indemnity obligations | uri: examples/clauses/sources/enterprise_saas_msa.md#L57-L58
atom ExceedLiabilityCap: Vendor pays or is liable for amounts above the aggregate liability cap | quote: capped at the fees paid | uri: examples/clauses/sources/enterprise_saas_msa.md#L56-L57

# ---------------------------------------------------------------------------
# Termination and wind-down
# ---------------------------------------------------------------------------
atom NinetyDayNotice: a party has given ninety (90) days' written notice of termination for convenience | quote: ninety (90) days' written notice | uri: examples/clauses/sources/enterprise_saas_msa.md#L62-L63
atom TerminateForConvenience: a party terminates the Agreement for convenience | quote: terminate for convenience | uri: examples/clauses/sources/enterprise_saas_msa.md#L62-L63
atom UncuredAfterNotice: a material breach was not cured within thirty (30) days after notice | quote: not cured within thirty (30) days after notice | uri: examples/clauses/sources/enterprise_saas_msa.md#L63-L64
atom TerminateForCause: a party terminates the Agreement for cause | quote: terminate for cause | uri: examples/clauses/sources/enterprise_saas_msa.md#L63-L64
atom AgreementTerminated: the Agreement has terminated | quote: Upon termination | uri: examples/clauses/sources/enterprise_saas_msa.md#L64-L65
atom ReturnOrDeleteCustomerData: Vendor returns or deletes Customer Data as Customer instructs | quote: return or delete Customer Data as instructed | uri: examples/clauses/sources/enterprise_saas_msa.md#L64-L65
atom AllowDataExportWindDown: Vendor provides a limited wind-down period for Customer to export data | quote: limited wind-down period for export | uri: examples/clauses/sources/enterprise_saas_msa.md#L65-L66

# ---------------------------------------------------------------------------
# Non-solicitation, insurance, audit
# ---------------------------------------------------------------------------
atom SolicitVendorEmployee: Customer solicits a Vendor employee for employment | quote: shall not solicit for employment any Vendor employee | uri: examples/clauses/sources/enterprise_saas_msa.md#L70-L71
atom EmployeeInitiatedContact: the Vendor employee initiated contact without Customer solicitation | quote: employee initiates contact without solicitation | uri: examples/clauses/sources/enterprise_saas_msa.md#L71-L72
atom MaintainInsurance: Vendor maintains commercially reasonable insurance | quote: maintain commercially reasonable insurance | uri: examples/clauses/sources/enterprise_saas_msa.md#L76-L77
atom ReasonableAuditNotice: Customer has given reasonable notice of a compliance audit | quote: Upon reasonable notice | uri: examples/clauses/sources/enterprise_saas_msa.md#L77-L78
atom CooperateWithAudit: Vendor cooperates with Customer's audit of security and data-processing compliance | quote: may audit Vendor's compliance | uri: examples/clauses/sources/enterprise_saas_msa.md#L77-L79

# ---------------------------------------------------------------------------
# Rules — license and scope
# ---------------------------------------------------------------------------
license_grant: OrderFormExecuted, CustomerParty  =>  ValidSubscriptionLicense
no_use_default:  =>O  ~UseSoftware
use_permitted: ValidSubscriptionLicense  ~>O  UseSoftware
scope_limit:  =>O  ~ExceedOrderScope
scope_is_breach: ExceedOrderScope  =>  MaterialBreach

# Fees
pay_when_due: FeesDue  =>O  PayFees
overdue_suspend: PaymentOverdue  =>O  SuspendAccess * PayOverdueAmounts * RestoreAccess
overdue_material: PaymentOverdue  =>  MaterialBreach

# SLA — uptime when active; credits only once failure is in the facts (sole remedy)
sla_uptime: ActiveSla  =>O  MeetUptimeTarget
sla_credits: SlaFailure, ActiveSla  =>O  ClaimServiceCredits

# Confidentiality carve-outs (pattern from disclosure_awareness / trade_secret)
conf_no_disclose:  =>O  ~DiscloseConfidentialInfo
conf_employees: EmployeeNeedToKnow, EmployeeUnderNDA  ~>O  DiscloseConfidentialInfo
conf_legal: LegalCompulsionRequired  ~>O  DiscloseConfidentialInfo

# DPA
dpa_no_process:  =>O  ~ProcessPersonalData
dpa_instruction: LawfulDataInstruction  ~>O  ProcessPersonalData
dpa_no_sub:  =>O  ~EngageSubprocessor
dpa_sub_notice: SubprocessorNoticeGiven  ~>O  EngageSubprocessor

# Security
sec_measures:  =>O  ImplementSecurityMeasures
sec_notify_remedy: SecurityIncident  =>O  NotifyCustomer * RemediateIncident

# Indemnity vs cap — excluded liabilities defeat the general cap on excess payments
indemnify_breach: VendorMaterialBreach, ThirdPartyClaim  =>O  IndemnifyCustomer
indemnify_ip: IpInfringementClaim  =>O  IndemnifyCustomer
cap_no_excess: LiabilityCapApplies  =>O  ~ExceedLiabilityCap
cap_excluded: ExcludedLiability  ~>O  ExceedLiabilityCap

# Termination
term_conv: NinetyDayNotice  ~>O  TerminateForConvenience
term_cause: MaterialBreach, UncuredAfterNotice  ~>O  TerminateForCause
post_term_data: AgreementTerminated  =>O  ReturnOrDeleteCustomerData
post_term_winddown: AgreementTerminated  ~>O  AllowDataExportWindDown

# Non-solicit, insurance, audit
no_solicit:  =>O  ~SolicitVendorEmployee
solicit_exception: EmployeeInitiatedContact  ~>O  SolicitVendorEmployee
insurance:  =>O  MaintainInsurance
audit_coop: ReasonableAuditNotice  =>O  CooperateWithAudit

# ---------------------------------------------------------------------------
# Superiority — specific permissions and exclusions defeat general defaults
# ---------------------------------------------------------------------------
superiority: use_permitted > no_use_default, conf_employees > conf_no_disclose, conf_legal > conf_no_disclose, dpa_instruction > dpa_no_process, dpa_sub_notice > dpa_no_sub, cap_excluded > cap_no_excess, solicit_exception > no_solicit

# ---------------------------------------------------------------------------
# CLI checks (run after uncommenting a scenario's facts: or copy facts: line)
#
#   deontic check examples/clauses/enterprise_saas_msa.ddl
#   deontic query examples/clauses/enterprise_saas_msa.ddl SuspendAccess RestoreAccess --trace
#   deontic query examples/clauses/enterprise_saas_msa.ddl ClaimServiceCredits MeetUptimeTarget
#   deontic abduce examples/clauses/enterprise_saas_msa.ddl 'P(DiscloseConfidentialInfo)' \
#       --assume EmployeeNeedToKnow,EmployeeUnderNDA
#     (large atom set — use --assume to pin carve-out paths; LegalCompulsion alone also suffices)
#   deontic abduce examples/clauses/enterprise_saas_msa.ddl 'P(SolicitVendorEmployee)' --all
#   deontic query examples/clauses/enterprise_saas_msa.ddl ExceedLiabilityCap IndemnifyCustomer
#
# Open questions (judge) — left unresolved on purpose:
# - Whether SlaFailure should defeasibly block sla_uptime (not modelled); a judge
#   might add `sla_credits > sla_uptime` if both O(MeetUptime) and O(ClaimCredits) clash.
# - post_term_winddown vs ReturnOrDeleteCustomerData if Customer instructs immediate
#   deletion with no export window — not modelled (needs priority facts).
# ---------------------------------------------------------------------------
