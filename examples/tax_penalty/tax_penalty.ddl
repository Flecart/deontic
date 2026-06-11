# FA 2009 Schedule 55 — late-filing penalties (domain #3 of the dataset)
# ---------------------------------------------------------------------------
# The most formulaic FTT jurisdiction: was the return late, was the penalty
# validly assessed and notified, is there a reasonable excuse, do special
# circumstances apply. Decision atom: PayPenalty (gold withhold-analogue =
# penalty UPHELD -> O(PayPenalty); gold disclose-analogue = penalty CANCELLED
# -> P(PayPenalty), the duty never arising).
# Deliberate v1 simplifications (documented): penalty AMOUNT variation is out
# of scope (binary upheld/cancelled per penalty); the para 16 special-
# circumstances route is modelled as a duty defeater although in law it is an
# HMRC discretion the tribunal reviews only for flawed decisions.
facts:

atom FilingObligationNotified: His Majesty's Revenue and Customs gave the taxpayer a notice requiring a return with a specified filing date (the obligation must exist and have been communicated). FALSE if no valid notice to file was given | quote: P fails to make or deliver a return | uri: examples/tax_penalty/sources/fa2009_sch55.md#L6-L9
atom ReturnLate: the taxpayer failed to make or deliver the return on or before the filing date. TRUE on any failure by the deadline, however short; FALSE if the return was on time or the obligation had been withdrawn | quote: on or before the filing date | uri: examples/tax_penalty/sources/fa2009_sch55.md#L6-L9
atom PenaltyAssessedNotified: the penalty was validly assessed and notice of it was given to the taxpayer, identifying the period and amount. FALSE where the assessment or its notification was procedurally invalid | quote: P is liable to a penalty under this paragraph | uri: examples/tax_penalty/sources/fa2009_sch55.md#L11-L13
atom PayPenalty: the taxpayer pays the assessed late-filing penalty. The decision atom — never assert it as a fact | quote: A penalty is payable by a person | uri: examples/tax_penalty/sources/fa2009_sch55.md#L6-L9
atom ReasonableExcuse: throughout the period of default the taxpayer had a reasonable excuse for the failure — an unexpected or unusual event, or reliance reasonably placed, such that a reasonable taxpayer conscious of their obligations and in the taxpayer's position would also have failed. An insufficiency of funds is NOT a reasonable excuse unless attributable to events outside the taxpayer's control; reliance on another person is NOT a reasonable excuse unless the taxpayer took reasonable care to avoid the failure | quote: an insufficiency of funds is not a reasonable excuse | uri: examples/tax_penalty/sources/fa2009_sch55.md#L28-L38
atom ExcuseRemediedPromptly: if the excuse ceased before the return was filed, the failure was remedied without unreasonable delay after it ceased (if the excuse persisted until filing, this is satisfied) | quote: remedied without unreasonable delay after the excuse ceased | uri: examples/tax_penalty/sources/fa2009_sch55.md#L28-L38
atom SpecialCircumstances: special circumstances exist — uncommon or exceptional factors making the penalty plainly inappropriate — AND the tribunal found HMRC's contrary special-circumstances decision flawed, so the penalty falls to be cancelled on this ground | quote: If HMRC think it right because of special circumstances | uri: examples/tax_penalty/sources/fa2009_sch55.md#L22-L26

# Liability: trigger + valid assessment.
duty_pay: FilingObligationNotified, ReturnLate, PenaltyAssessedNotified  =>O@Taxpayer  PayPenalty

# Defences are duty blockers: liability never arises (P, not F).
excuse_block:  ReasonableExcuse, ExcuseRemediedPromptly  ~>O@Taxpayer  ~PayPenalty
special_block: SpecialCircumstances  ~>O@Taxpayer  ~PayPenalty

superiority: excuse_block > duty_pay, special_block > duty_pay
