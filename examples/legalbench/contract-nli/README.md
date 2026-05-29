# LegalBench contract_nli — formalized as DDL

One `.ddl` theory per [LegalBench](https://hazyresearch.stanford.edu/legalbench/)
`contract_nli_*` task (the [ContractNLI](https://stanfordnlp.github.io/contract-nli/)
NDA benchmark). Each file encodes the relevant NDA provision; running the
reasoner decides the task's hypothesis. Hypothesis texts (with line numbers used
as provenance) are in [`sources/hypotheses.md`](sources/hypotheses.md). See
[`BASELINE.md`](BASELINE.md) for whether/how the reasoner helps.

Run from the project root (`PATH="$HOME/.elan/bin:$PATH"`,
`B=./.lake/build/bin/deontic`).

| Task (file) | Pattern | Test | Result | Label |
|-------------|---------|------|--------|-------|
| limited_use | prohibition | `$B query …/limited_use.ddl UseForOtherPurpose` | `F(UseForOtherPurpose)` | Entail |
| confidentiality_of_agreement | prohibition | `query … DiscloseAgreementExistence` | `F(…)` | Entail |
| no_licensing | prohibition | `query … AcquireRightsInCI` | `F(…)` | Entail |
| notice_on_compelled_disclosure | cond. obligation | `query … NotifyDisclosingParty` | `O(…)` | Entail |
| return_of_confidential_information | cond. obligation | `query … ReturnOrDestroyCI` | `O(…)` | Entail |
| survival_of_obligations | constitutive | `query … ObligationsSurviveTermination` | `fact(…)` | Entail |
| sharing_with_employees | permission carve-out | `abduce … 'P(Disclose)' --all` | `{ EmployeeRecipient }` | Entail |
| sharing_with_third-parties | permission carve-out | `abduce … 'P(Disclose)' --all` | `{ ThirdPartyBoundByConfidentiality }` | Entail |
| permissible_acquirement_of_similar_information | permission carve-out | `abduce … 'P(UseSimilarInformation)' --all` | `{ AcquiredFromThirdParty }` | Entail |
| permissible_development_of_similar_information | permission carve-out | `abduce … 'P(UseSimilarInformation)' --all` | `{ IndependentlyDeveloped }` | Entail |
| permissible_copy | permission carve-out | `abduce … 'P(CopyCI)' --all` | `{ AuthorizedNeed }` | Entail |
| permissible_post-agreement_possession | permission carve-out | `abduce … 'P(RetainAfterTermination)' --all` | `{ ArchivalBackup }` | Entail |
| explicit_identification | constitutive (sole path) | `abduce … 'C(ConfidentialInformation)' --all` | `{ MarkedConfidential }` | Entail |
| inclusion_of_verbally_conveyed_information | constitutive | `abduce … 'C(ConfidentialInformation)' --all` | `{ VerballyConveyed }` | Entail |

Each file encodes a contract for which the hypothesis is **entailed**. The other
ContractNLI labels follow the same kernel: *Contradiction* = the contract derives
the opposite (e.g. an unconditional `=>O Disclose` makes `F(Disclose)` underivable
and `O(Disclose)` derivable); *NotMentioned* = no rule addresses the atom, so
`query` returns `unknown` / `abduce` returns no configuration.
