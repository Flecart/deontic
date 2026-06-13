# Case-quality validation & the description-edit protocol

How every statute's cases are quality-checked, and the exact rule for when an
atom description may be edited. This is the answer to "how do you know the
cases are good?" and "under what criteria are you rewriting open/closed?".

## 1. Case-quality gates (every statute, before any result is read)

1. **Oracle gate.** Feed the *gold* atom assignment to the engine; it must
   reproduce the case's gold verdict on every case (asserted in `arms.py`).
   Confirms the harness and the gold computation. (576+ oracle rows per
   statute, all exact.)
2. **Program gate.** The no-LLM closed-ID lookup must score 100% verdict at
   Tier 0 and true-atom recall exactly 100/0/0 across tiers. Confirms the
   tiering (Tier-0 = listed, Tiers 1–2 = unlisted) is correctly constructed.
3. **Leak check.** Each narration is rejected (and excluded from scoring) if
   it contains any atom name, any statute-vocabulary stem, any 5-gram of an
   open description (all tiers), or of a closed description (Tiers 1–2).
   Confirms the answer cannot be read off the prose.
4. **Bank validation.** Two annotator models from families *disjoint from the
   narrator and the grounders* judge every bank item against the **open
   intension**, standalone and blind to tier. High agreement = the gold
   labels are not idiosyncratic to the author; disagreements are inspected
   (gate 6).
5. **Verdict-class stratification + narrator isolation.** Cases are sampled
   balanced across gold verdict classes; the narrator is a third family that
   never sees the gold (backward generation makes narrations outcome-free by
   construction, so there is nothing to leak).
6. **The audit loop.** Two disagreement signatures are treated as *our* bugs,
   not model errors:
   - *grounder right where gold is wrong* → a world-model defect (e.g. an
     incoherent distractor, an emergency narrated as an adjacent matter).
   - *annotator right where gold is wrong* → a **description defect** (the
     intension is genuinely ambiguous/underspecified). This is the only
     trigger that licenses a description edit — see §2.

## 2. When (and only when) an atom description may be edited

The canonical descriptions are **frozen before generation**; gold is defined
by the open intension. A description may be edited *only* under all of:

1. **Trigger = blind bank validation, never a grounding score.** The edit is
   licensed by independent annotators (gate 4) systematically disagreeing
   with the author's gold *and being right* — i.e. the intension is
   genuinely ambiguous. It is **never** licensed by "a grounder got a low
   number." Editing because a model underperformed would be fishing; editing
   because two blind annotators show the text is ambiguous is QA.
2. **The edit removes ambiguity, it does not add extension.** An open
   description must stay an intension — naming a missing *scope/condition*
   (e.g. "the procurement purpose", "the period of the draw") is allowed;
   adding enumerated *instances* is not (that would convert open→closed and
   contaminate the comparison). Closed descriptions are eligible for the same
   ambiguity fix, but in practice an explicit enumeration is rarely flagged
   ambiguous.
3. **It is logged and disclosed.** Each edit is recorded (a `NOTES_*.txt` in
   the statute dir) with the before/after text, the triggering disagreement,
   and the measured effect; the paper discloses it.
4. **Direction-independence is checked.** We report whether the headline
   (open > closed at Tier 2) already held on the *un-repaired* run. If a fix
   only ever helped the thesis, that would be a red flag; we state when it
   does not (e.g. expD: the gap was positive pre-fix too).

### Ordering rule (the clean way, enforced going forward)

Run gates 1–4 **before** grounding: validate the banks, fix any
ambiguity-flagged description, *then* freeze and run grounding. Statute B
followed this order (the `allocation_granted` temporal-scope fix preceded the
grounding run — clean). Statute D did not: the `within_scope` ambiguity was
caught by validation that ran *after* the main grounding, so grounding was
re-run on the fixed description. The trigger was still blind validation (not a
score), the gap was positive pre-fix, and it is fully disclosed — but the
post-hoc ordering is why it needed extra disclosure, and it is the reason the
ordering rule above is now mandatory.

### What the edits were, to date (full list)

- **B / `allocation_granted`** (pre-grounding, clean): "...at some point
  granted..." → "...granted an entitlement that covers this category *and the
  period of the draw*...". A lapsed voucher otherwise satisfied the
  intension. Trigger: both annotators agreed the original was too broad.
- **D / `within_scope`** (post-grounding, re-run + disclosed): "...judged by
  the purpose the mandate serves..." → named the procurement/supply domain.
  The original never said *what* purpose, so it was unbounded. Trigger: blind
  validation (one annotator over-read, one under-read).

### Not in this category: the `open2` redraft *experiment*

The evidentiary redrafts of `anonymized`/`emergency`/`offset_posted` are a
**separate, labeled repair experiment** (a reported arm, `ground_open2`), not
a silent edit of the canonical open description. They test whether a
pathological epistemic-bar intension can be repaired by re-stating it to
judge described evidence rather than unobservable fact. They are reported
as their own result (including where the repair *hurt* — `offset_posted`),
never folded into the headline open numbers.

## Why open gets "helped" more than closed by these fixes (and why that is
## a finding, not a thumb on the scale)

An under-specified intension *under-grounds* (a model can't apply a vague
standard); an explicit enumeration has no such failure mode, so the same
ambiguity fix moves open a lot and closed barely. That asymmetry is the
thesis in miniature — "an open standard is only as good as its
specification" — not evidence of tuning, *provided* the fix is
ambiguity-driven (gate 4) and enumeration-free (§2.2). The protocol exists to
keep that line bright.
