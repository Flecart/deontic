# LegalBench cuad — deontic clause types as DDL

Representative formalizations of the **deontic** [CUAD](https://www.atticusprojectai.org/cuad)
clause categories used by LegalBench `cuad_*` tasks. Same approach as
[`../contract-nli/`](../contract-nli/): one `.ddl` per clause type, mandatory
atom descriptions + provenance into [`sources/clauses.md`](sources/clauses.md),
and a footer test. (`B=./.lake/build/bin/deontic`, run from project root.)

| Task (file) | Pattern | Test | Result |
|-------------|---------|------|--------|
| cuad_non-compete | prohibition | `$B query … Compete` | `F(Compete)` |
| cuad_no-solicit-of-employees | prohibition | `$B query … SolicitEmployees` | `F(…)` |
| cuad_covenant-not-to-sue | prohibition | `$B query … Sue` | `F(Sue)` |
| cuad_audit-rights | obligation | `$B query … PermitAudit` | `O(PermitAudit)` |
| cuad_insurance | obligation | `$B query … MaintainInsurance` | `O(…)` |
| cuad_anti-assignment | permission carve-out | `$B abduce … 'P(Assign)' --all` | `{ PriorWrittenConsent }` |
| cuad_termination-for-convenience | permission carve-out | `$B abduce … 'P(Terminate)' --all` | `{ NoticeGiven }` |
| cuad_exclusivity | prohibition | `$B query … DealWithCompetitors` | `F(…)` |
| cuad_most-favored-nation | obligation | `$B query … OfferNoLessFavorableTerms` | `O(…)` |
| cuad_minimum-commitment | obligation | `$B query … MeetMinimumPurchase` | `O(…)` |
| cuad_post-termination-services | cond. obligation | `$B query … ProvideTransitionServices` | `O(…)` |
| cuad_rofr | permission carve-out | `$B abduce … 'P(SellToThirdParty)' --all` | `{ OfferedToHolderFirst }` |
| cuad_non-disparagement | prohibition | `$B query … Disparage` | `F(Disparage)` |
| cuad_indemnification | cond. obligation | `$B query … Indemnify` | `O(Indemnify)` |
| cuad_license-grant | permission | `$B query … UseLicensedSoftware` | `Ps(UseLicensedSoftware)` |
| cuad_change-of-control | permission carve-out | `$B abduce … 'P(TerminateOnChangeOfControl)' --all` | `{ ChangeOfControl }` |
| cuad_termination-for-cause | permission carve-out | `$B abduce … 'P(TerminateForCause)' --all` | `{ MaterialBreach }` |
| cuad_non-transferability | prohibition | `$B query … Transfer` | `F(Transfer)` |
| cuad_source-code-escrow | cond. obligation | `$B query … ReleaseSourceCode` | `O(…)` |
| cuad_liquidated-damages | cond. obligation | `$B query … PayLiquidatedDamages` | `O(…)` |

These cover CUAD's clause types that express a duty, prohibition, or
conditional permission. Purely descriptive CUAD categories (governing law,
liability cap, IP-ownership, …) aren't deontic and are out of scope for this
reasoner. See [`../COMPARISON.md`](../COMPARISON.md) for the with/without-reasoner
baseline protocol.
