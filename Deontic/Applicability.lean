import Deontic.Theory
import Deontic.ProofTags

namespace Deontic

-- ── Body applicability (§3.3 p.18) ───────────────────────────────────────────
--
-- A rule r is body-applicable iff for all ai ∈ A(r):
--   1. if ai = □l  then  +∂_□ l ∈ P(1..n)
--   2. if ai = ¬□l then  -∂_□ l ∈ P(1..n)
--   3. if ai = l ∈ Lit then l ∈ F

private def checkLiteral (d : Derivation) (facts : List Lit) (l : Literal) (want : Bool) : Bool :=
  match l with
  | .plain pl =>
    if want then facts.contains pl
    else !(facts.contains pl)
  | .deontic dl =>
    let mod : Modality := match dl.op with
      | .O  => .O
      | .F  => .O   -- F l = O ~l, so we look for O on the complement
      | .P  => .P
      | .Pw => .Pw
      | .Ps => .Ps
    let lit : Lit := match dl.op with
      | .F => dl.lit.compl   -- F(l) means O(~l)
      | _  => dl.lit
    d.has ⟨want, mod, none, lit⟩

def bodyApplicable (r : Rule) (d : Derivation) (facts : List Lit) : Bool :=
  r.antecedent.all (checkLiteral d facts · true)

def bodyDiscarded (r : Rule) (d : Derivation) (facts : List Lit) : Bool :=
  r.antecedent.any (checkLiteral d facts · false)

-- ── Body-p-applicable (§3.3 p.18) ────────────────────────────────────────────
--
-- r is body-p-applicable iff:
--   1. r ∈ R^O and it is body-applicable, or
--   2. r ∈ R^C and A(r) ≠ ∅, A(r) ⊆ PLit, and ∀ai ∈ A(r), +∂_O ai ∈ P(1..n)

def bodyPApplicable (r : Rule) (d : Derivation) (facts : List Lit) : Bool :=
  match r.family with
  | .prescriptive => bodyApplicable r d facts
  | .constitutive =>
    !r.antecedent.isEmpty &&
    r.antecedent.all (fun l => match l with | .plain _ => true | .deontic _ => false) &&
    r.antecedent.all (fun l => match l with
      | .plain pl => d.hasPositive .O pl
      | .deontic _ => false)

-- r is body-p-discarded iff:
--   1. r ∈ R^O and it is not body-applicable, or
--   2. r ∈ R^C and either A(r) = ∅ or A(r) ∩ DLit ≠ ∅
--      or ∃ai ∈ A(r), -∂_O ai ∈ P(1..n)

def bodyPDiscarded (r : Rule) (d : Derivation) (facts : List Lit) : Bool :=
  match r.family with
  | .prescriptive => bodyDiscarded r d facts
  | .constitutive =>
    r.antecedent.isEmpty ||
    r.antecedent.any (fun l => match l with | .deontic _ => true | .plain _ => false) ||
    r.antecedent.any (fun l => match l with
      | .plain pl => d.hasNegative .O pl
      | .deontic _ => false)

-- ── Applicable for index (§3.3 p.18-19) ──────────────────────────────────────
--
-- r ∈ R[q,j] is applicable for literal q at index j (1 ≤ j < n) iff:
--   1. r is body-p-applicable, and
--   2. for all ck ∈ C(r), 1 ≤ k < j: +∂_O ck ∈ P(1..n) and (ck ∉ F or ~ck ∈ F)
--
-- This captures that every earlier element in the ⊗-chain is obligatory
-- AND has been violated (its negation is a fact).

def applicableForIndex (r : Rule) (q : Lit) (j : Nat) (d : Derivation) (facts : List Lit) : Bool :=
  -- verify q appears at position j in conclusion
  let atJ := r.conclusion[j]? == some q
  atJ &&
  bodyPApplicable r d facts &&
  -- all ck at index k < j must be obligatory with a violation
  (r.conclusion.zipIdx.filter (fun (_, k) => k < j)).all fun (ck, _) =>
    d.hasPositive .O ck && (!(facts.contains ck) || facts.contains ck.compl)

end Deontic
