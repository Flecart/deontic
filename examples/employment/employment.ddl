# ERA 1996 unfair dismissal — formalization (domain #4 of the dataset)
# ---------------------------------------------------------------------------
# Structure: the s94 right creates a default that a qualifying dismissal is
# unfair (the burden architecture of s98 — the employer must show a fair
# reason AND s98(4) reasonableness to escape); an automatically unfair reason
# (s99-105) cannot be saved by reasonableness and needs no qualifying period.
# Decision atom: FindUnfair, borne by @Tribunal (the codice_penale @Giudice
# pattern). Gold mapping: claim succeeds -> O(FindUnfair) ("unfair");
# employer's defence holds -> P(FindUnfair) ("fair").
# v1 scope: liability only (fair/unfair); remedy, Polkey deductions, and
# contributory fault are out of scope. Constructive dismissal folds into
# Dismissed's contract.
facts:

atom Dismissed: the employee was dismissed by the employer — the contract was terminated by the employer (with or without notice), a limited-term contract expired without renewal, or the employee resigned in circumstances entitling them to do so because of the employer's repudiatory breach (constructive dismissal). FALSE for a genuine voluntary resignation or consensual termination | quote: An employee has the right not to be unfairly dismissed | uri: examples/employment/sources/era_1996.md#L6-L9
atom QualifyingService: the employee had been continuously employed for at least two years ending with the effective date of termination. FALSE for shorter service — unless the claimed reason is automatically unfair, which needs no qualifying period (assert AutomaticallyUnfairReason instead) | quote: continuously employed for at least two years | uri: examples/employment/sources/era_1996.md#L38-L48
atom FairReasonShown: the employer showed the reason (or principal reason) for the dismissal, and it is a potentially fair one — it relates to the employee's capability or qualifications for the work, relates to the employee's conduct, is redundancy, is a statutory restriction making continued employment unlawful, or is some other substantial reason of a kind justifying dismissal from that position. FALSE if the employer failed to establish what the real reason was, or the reason shown is none of these | quote: a reason falling within subsection (2) or some other substantial reason | uri: examples/employment/sources/era_1996.md#L11-L25
atom ReasonableResponse: in the circumstances (including the employer's size and administrative resources) the employer acted reasonably in treating the shown reason as sufficient for dismissal, judged by equity and the substantial merits: the decision fell within the band of reasonable responses open to a reasonable employer (not what the tribunal itself would have done), and a fair procedure was followed — for conduct, a genuine belief in the misconduct, held on reasonable grounds, after a reasonable investigation. FALSE where the sanction was outside the band, the investigation or process was unfair, or the belief lacked reasonable grounds | quote: acted reasonably or unreasonably in treating it as a sufficient reason | uri: examples/employment/sources/era_1996.md#L27-L36
atom AutomaticallyUnfairReason: the reason (or principal reason) for the dismissal was one the statute makes automatically unfair — e.g. pregnancy or family leave, health-and-safety activities, making a protected whistleblowing disclosure, trade-union membership or activities, or asserting a statutory right. No reasonableness assessment applies and no qualifying period is required | quote: the qualifying period does not apply where the reason is one of the automatically unfair reasons | uri: examples/employment/sources/era_1996.md#L38-L48
atom FindUnfair: the tribunal finds the dismissal unfair. The decision atom — never assert it as a fact | quote: An employee has the right not to be unfairly dismissed | uri: examples/employment/sources/era_1996.md#L6-L9

# Default: a qualifying dismissal is unfair unless the employer's defence holds.
unfair_default: Dismissed, QualifyingService  =>O@Tribunal  FindUnfair

# The employer's s98 defence: fair reason + s98(4) reasonableness.
fair_block: FairReasonShown, ReasonableResponse  ~>O@Tribunal  ~FindUnfair

# Automatically unfair reasons: unfair regardless of the defence, no
# qualifying period.
auto_unfair: Dismissed, AutomaticallyUnfairReason  =>O@Tribunal  FindUnfair

superiority: fair_block > unfair_default, auto_unfair > fair_block
