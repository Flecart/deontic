import Deontic.Theory
import Deontic.ProofTags
import Deontic.Applicability

namespace Deontic

-- ── Helpers ───────────────────────────────────────────────────────────────────

private def firstIndex (l : List Lit) (q : Lit) : Nat :=
  l.findIdx (· == q)

private def discardedOrDefeated
    (thy : Theory) (d : Derivation) (s : Rule) (rulesForQ : List Rule) : Bool :=
  bodyDiscarded s d thy.facts ||
  rulesForQ.any fun t =>
    bodyApplicable t d thy.facts && thy.defeats t.label s.label

private def pDiscardedOrDefeated
    (thy : Theory) (d : Derivation) (s : Rule) (rulesForQ : List Rule) : Bool :=
  bodyPDiscarded s d thy.facts ||
  rulesForQ.any fun t =>
    (bodyApplicable t d thy.facts || bodyPApplicable t d thy.facts) &&
    thy.defeats t.label s.label

-- Non-defeater rules concluding q (used by O proof conditions — defeaters cannot
-- positively establish obligations, §3.1)
def obligatoryRulesFor (thy : Theory) (q : Lit) : List Rule :=
  thy.rules.filter fun r =>
    r.conclusion.any (· == q) && r.strength != .defeater

-- Prescriptive rules that are body-p-applicable for literal q at its conclusion index.
def applicableObligationRules (thy : Theory) (d : Derivation) (q : Lit) : List Rule :=
  obligatoryRulesFor thy q |>.filter fun r =>
    let j := firstIndex r.conclusion q
    applicableForIndex r q j d thy.facts

-- ── +∂_C (§3.3 p.19) ─────────────────────────────────────────────────────────

def canDerive_C_pos (thy : Theory) (d : Derivation) (q : Lit) : Bool :=
  if thy.facts.contains q then true
  else
    let constitForQ := thy.constitutiveRules.filter (fun r =>
      r.conclusion.head? == some q && r.strength != .defeater)
    let anyApplicable := constitForQ.any (bodyApplicable · d thy.facts)
    let applicableForQ := constitForQ.filter (bodyApplicable · d thy.facts)
    let allCounterDefeated := thy.rulesFor q.compl |>.all fun s =>
      discardedOrDefeated thy d s applicableForQ
    !thy.facts.contains q.compl && anyApplicable && allCounterDefeated

-- ── -∂_C (strong negation of +∂_C) ───────────────────────────────────────────

def canDerive_C_neg (thy : Theory) (d : Derivation) (q : Lit) : Bool :=
  if thy.facts.contains q then false
  else
    let constitForQ := thy.constitutiveRules.filter (fun r =>
      r.conclusion.head? == some q && r.strength != .defeater)
    let allDiscarded := constitForQ.all (bodyDiscarded · d thy.facts)
    let existsUndefeated := thy.rulesFor q.compl |>.any fun s =>
      bodyApplicable s d thy.facts &&
      constitForQ.all fun t =>
        bodyDiscarded t d thy.facts || !thy.defeats t.label s.label
    thy.facts.contains q.compl || allDiscarded || existsUndefeated

-- ── +∂_O (§3.3 p.19-20) ──────────────────────────────────────────────────────
-- Only strict/defeasible rules (not defeaters) can establish obligations

def canDerive_O_pos (thy : Theory) (d : Derivation) (q : Lit) : Bool :=
  let candidateRules := obligatoryRulesFor thy q
  let anyApplicable := candidateRules.any fun r =>
    let j := firstIndex r.conclusion q
    applicableForIndex r q j d thy.facts
  if !anyApplicable then false
  else
    let applicableRules := candidateRules.filter fun r =>
      bodyApplicable r d thy.facts || bodyPApplicable r d thy.facts
    thy.rulesFor q.compl |>.all fun s =>
      pDiscardedOrDefeated thy d s applicableRules

-- ── -∂_O (strong negation of +∂_O) ───────────────────────────────────────────

def canDerive_O_neg (thy : Theory) (d : Derivation) (q : Lit) : Bool :=
  let candidateRules := obligatoryRulesFor thy q
  let allNotApplicable := candidateRules.all fun r =>
    let j := firstIndex r.conclusion q
    !applicableForIndex r q j d thy.facts
  if allNotApplicable then true
  else
    let applicableRules := candidateRules.filter fun r =>
      bodyApplicable r d thy.facts || bodyPApplicable r d thy.facts
    thy.rulesFor q.compl |>.any fun s =>
      (bodyApplicable s d thy.facts || bodyPApplicable s d thy.facts) &&
      applicableRules.all fun t =>
        !thy.defeats t.label s.label

-- ── +∂_Ps (§3.3 p.20) ────────────────────────────────────────────────────────
-- Strong permission: either inherited from obligation, or an undefeated defeater
-- for q blocks O(~q).  The defeater is in R[q] (concludes q), not R[~q].

def canDerive_Ps_pos (thy : Theory) (d : Derivation) (q : Lit) : Bool :=
  if d.hasPositive .O q then true
  else
    thy.defeatersOf.filter (fun r => r.conclusion.head? == some q)
      |>.any fun r =>
        let bodyOk := bodyPApplicable r d thy.facts
        let counterDefeated := thy.rulesFor q.compl |>.all fun s =>
          let discarded := bodyPDiscarded s d thy.facts
          let defeatedBySome :=
            thy.rules.filter (fun t =>
              t.conclusion.any (· == q) && bodyApplicable t d thy.facts)
            |>.any (fun t => thy.defeats t.label s.label)
          discarded || defeatedBySome
        bodyOk && counterDefeated

-- ── -∂_Ps (strong negation) ───────────────────────────────────────────────────

def canDerive_Ps_neg (thy : Theory) (d : Derivation) (q : Lit) : Bool :=
  !canDerive_Ps_pos thy d q && d.hasNegative .O q

-- ── +∂_Pw (§3.3 p.20) ────────────────────────────────────────────────────────

def canDerive_Pw_pos (d : Derivation) (q : Lit) : Bool :=
  d.hasNegative .O q.compl

-- ── -∂_Pw (strong negation) ───────────────────────────────────────────────────
-- If O(~q) is established, weak permission of q fails

def canDerive_Pw_neg (d : Derivation) (q : Lit) : Bool :=
  d.hasPositive .O q.compl

-- ── +∂_P (§3.3 p.20) ─────────────────────────────────────────────────────────

def canDerive_P_pos (d : Derivation) (q : Lit) : Bool :=
  d.hasPositive .Ps q || d.hasPositive .Pw q

-- ── -∂_P (strong negation) ───────────────────────────────────────────────────

def canDerive_P_neg (d : Derivation) (q : Lit) : Bool :=
  d.hasNegative .Ps q && d.hasNegative .Pw q

-- ── +∂_⊥ (§3.3 p.21) ─────────────────────────────────────────────────────────

-- A literal ci is "violated" in the facts:
--   pos a: a should hold but doesn't (a ∉ F)
--   neg a: a should not hold but does (pos a ∈ F)
private def isViolatedInFacts (facts : List Lit) (ci : Lit) : Bool :=
  match ci with
  | .pos a => !facts.contains (.pos a)
  | .neg a => facts.contains (.pos a)

def canDerive_bot (thy : Theory) (d : Derivation) : Bool :=
  thy.rules.filter (fun r => r.strength != .strict)
    |>.any fun r =>
      bodyPApplicable r d thy.facts &&
      !r.conclusion.isEmpty &&
      r.conclusion.all fun ci =>
        d.hasPositive .O ci && isViolatedInFacts thy.facts ci

end Deontic
