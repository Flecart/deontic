# ============================================================
# NDA confidentiality clause — disclosure limitation + standard of care
# ============================================================

facts: {{FACTS_FILLED_BY_FACT_FINDER}}

# --- Constitutive: who counts as a Representative ---
def1: Director  => RecipientIsRepresentative
def2: Officer  => RecipientIsRepresentative
def3: Employee  => RecipientIsRepresentative
def4: Agent  => RecipientIsRepresentative

# --- Prescriptive: default prohibition on disclosure ---
rprohibit:  =>O  ~Disclose

# --- Permission carve-out: Representative + need-to-know + solely Transaction purpose ---
rperm: RecipientIsRepresentative, NeedToKnow, TransactionPurpose  ~>O  Disclose

# --- Standard of care (cumulative, non-conflicting) ---
rcare:   =>O  Protect
rfloor:  =>O  ReasonableEfforts

superiority: rperm > rprohibit

# ============================================================
# RULES SUMMARY
# ============================================================
# def1-def4 : A director, officer, employee, or agent counts as a Representative.
# rprohibit : By default, Confidential Information must not be disclosed.
# rperm     : Disclosure is permitted when the recipient is a Representative
#             with a need to know, solely for the Transaction.
# rcare     : Must protect the CI to the same degree used for own trade secrets.
# rfloor    : Must in no event use less than reasonable efforts to protect the CI.
#
# ============================================================
# SUPERIORITY RATIONALE
# ============================================================
# rperm > rprohibit : The specific permission carve-out defeats the general
#   default prohibition when all three conditions hold; without it the defeater
#   would merely block ~Disclose, but explicit superiority makes the permission
#   outcome definitive.
#
# ============================================================
# OPEN QUESTIONS (judge decisions)
# ============================================================
# 1. Sentence 1 permits disclosure to the full Representative class for "the
#    Transaction"; sentence 2 narrows to "employees" for "authorized use". Is
#    sentence 2 an emphatic restatement, or a genuine narrowing that should
#    override (rperm conditioned on Employee + AuthorizedUse rather than
#    RecipientIsRepresentative + TransactionPurpose)? Current encoding silently
#    takes the broader s1 reading — matters for disclosure to an agent who is
#    not an employee.
# 2. Are "need to know" (s1) and "need for disclosure" (s2), and "the
#    Transaction" (s1) vs "authorized use" (s2), coextensive? Modeled as
#    coextensive (single NeedToKnow / TransactionPurpose atoms); split if the
#    contract treats them as distinct.
# 3. "only for that purpose" is folded into TransactionPurpose. If purpose-misuse
#    needs its own violable obligation (e.g. a separate O(~UseForOtherPurpose)),
#    break it out.
# 4. Standard of care modeled as two cumulative obligations (Protect =
#    own-trade-secret degree; ReasonableEfforts = absolute floor). The "no event
#    less than" floor that should *raise* a weaker own-secret practice is a
#    max-of-two-standards relation DDL won't express directly — handle in the
#    Protect atom's grounding or in 𝒥.
#
# ============================================================
# ENCODING NOTES
# ============================================================
# Core modeled as a default prohibition (rprohibit) plus a permission defeater
# (rperm), following the license/use reference pattern. rperm is a defeater
# (~>O) rather than a positive =>O because the clause grants leave to disclose,
# it does not mandate disclosure. The "collectively Representatives" definition
# is captured constitutively (def1-def4 => RecipientIsRepresentative); the
# enumeration's own catch-all "representatives" is omitted as self-referential —
# add a def5 stub if your fact-finder emits a generic Representative role. No
# compensatory chain (*) is used: the text describes a primary duty with
# conditions, not a remedy-after-breach. rcare and rfloor do not conflict (both
# simultaneously required), so no superiority is needed between them.