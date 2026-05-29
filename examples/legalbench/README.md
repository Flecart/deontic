# LegalBench tasks formalized as DDL

Formalizing [LegalBench](https://hazyresearch.stanford.edu/legalbench/) tasks
that have **deontic** content (obligations, prohibitions, permissions) as `.ddl`
theories, so the `deontic` reasoner can decide them — an auditable kernel in
place of, or alongside, direct LLM classification.

| Family | Dir | Coverage |
|--------|-----|----------|
| ContractNLI | [`contract-nli/`](contract-nli/) | 14 `contract_nli_*` tasks + NDA-2, contradiction / not-mentioned variants, and a combined multi-hypothesis NDA |
| CUAD | [`cuad/`](cuad/) | 24 deontic clause types (non-compete, audit-rights, anti-assignment, exclusivity, MFN, ROFR, indemnification, escrow, warranty, …) |
| Consumer contracts QA | [`consumer-contracts-qa/`](consumer-contracts-qa/) | 11 yes/no questions as permission/obligation queries |
| Privacy policy | [`privacy-policy/`](privacy-policy/) | 13 data-protection duties/rights (breach, deletion, access, sharing, retention, children, marketing, security, minimization, consent, transfer, DPIA, processor) |
| Telemarketing Sales Rule | [`telemarketing-sales-rule/`](telemarketing-sales-rule/) | 8 FTC TSR duties (do-not-call, calling hours, identification, robocall, abandoned calls, caller-id, cost disclosure, recordkeeping) |
| Contract QA | [`contract-qa/`](contract-qa/) | 5 employment/services yes/no questions (notice, at-will, overtime, confidentiality, reimbursement) |
| MAUD (merger agreements) | [`maud/`](maud/) | 7 deal-point covenants (ordinary-course, no-shop, best-efforts, fiduciary-out, financing, MAE, hell-or-high-water) + 2 label variants |
| Supply chain disclosure | [`supply-chain-disclosure/`](supply-chain-disclosure/) | 5 SB 657 disclosure duties (verification, audits, certification, accountability, training) |
| FDCPA (debt collection) | [`fdcpa/`](fdcpa/) | 5 debt-collector duties (unusual-time, harassment, false representation, validation notice, cease-on-request) |
| HIPAA (health privacy) | [`hipaa/`](hipaa/) | 4 Privacy Rule duties (minimum necessary, authorization, breach notice, accounting) |
| COPPA (children's privacy) | [`coppa/`](coppa/) | 5 operator duties (parental consent, notice, access, deletion, no-conditioning) |
| ECOA (credit anti-discrimination) | [`ecoa/`](ecoa/) | 4 creditor duties (no discrimination, no discouragement, count protected income, adverse-action notice) |
| Securities | [`securities/`](securities/) | 5 duties (insider trading, tipping, Reg FD, §16 reporting, short-swing) |
| FCRA (credit reporting) | [`fcra/`](fcra/) | 5 CRA/user duties (permissible purpose, accuracy, reinvestigation, adverse-action disclosure, no obsolete info) |
| CAN-SPAM (commercial email) | [`can-spam/`](can-spam/) | 5 sender duties (no false header, no deceptive subject, opt-out, honor opt-out, physical address) |
| Fair Housing Act | [`fair-housing/`](fair-housing/) | 5 housing duties (no refusal, terms, advertising, steering; reasonable accommodation) |
| ADA (disability) | [`ada/`](ada/) | 4 duties (no discrimination, reasonable accommodation, accessibility, interactive process) |

~139 deontic cases total, all verified. All three NLI labels (Entailment /
Contradiction / NotMentioned) are exercised across contract-nli, cuad, and maud.

[`COMPARISON.md`](COMPARISON.md) — baseline protocol & analysis: **with** the
reasoner (LLM → `.ddl` → `deontic`) vs **without** (direct LLM classification).

Each task file carries mandatory atom descriptions + provenance into a
`sources/` markdown (resolve with `deontic atoms --resolve`), and a footer
giving the `query`/`abduce` test and the expected label. Four patterns cover
every deontic hypothesis shape: prohibition (`=>O ~X`), conditional obligation
(`cond =>O X`), permission carve-out (`default + cond ~>O X + superiority`), and
constitutive classification (`cond => Y`).

Out of scope: non-deontic LegalBench tasks (issue-spotting, citation, pure
factual QA, descriptive clause categories) — they aren't normative-inference
problems.
