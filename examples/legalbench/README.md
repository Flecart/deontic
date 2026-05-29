# LegalBench tasks formalized as DDL

Formalizing [LegalBench](https://hazyresearch.stanford.edu/legalbench/) tasks
that have **deontic** content (obligations, prohibitions, permissions) as `.ddl`
theories, so the `deontic` reasoner can decide them — an auditable kernel in
place of, or alongside, direct LLM classification.

| Family | Dir | Coverage |
|--------|-----|----------|
| ContractNLI | [`contract-nli/`](contract-nli/) | 14 `contract_nli_*` tasks + NDA-2, contradiction / not-mentioned variants, and a combined multi-hypothesis NDA |
| CUAD | [`cuad/`](cuad/) | 15 deontic clause types (non-compete, audit-rights, anti-assignment, exclusivity, MFN, ROFR, indemnification, …) |
| Consumer contracts QA | [`consumer-contracts-qa/`](consumer-contracts-qa/) | 7 yes/no questions as permission/obligation queries |
| Privacy policy | [`privacy-policy/`](privacy-policy/) | 8 data-protection duties/rights (breach, deletion, access, sharing, retention, children, marketing, security) |
| Telemarketing Sales Rule | [`telemarketing-sales-rule/`](telemarketing-sales-rule/) | 4 FTC TSR duties (do-not-call, calling hours, identification, robocall consent) |

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
