import Deontic.Theory
import Deontic.ProofTags
import Deontic.Extension

namespace Deontic

/-!
# Abduction: which facts make a goal hold?

Given a theory and a *goal* (a tagged-literal status we want the extension to
entail, e.g. "O(use)" or "P(Disclose)"), search for the **fact configurations**
that make the goal hold.

This answers questions like:
  * "all the configurations that *allow* `Disclose`"  → goal `P(Disclose)`, `--all`
  * "some configurations that *require* `use`"        → goal `O(use)`
  * "can `Disclose` hold while `Notify` does not?"     → goal `P(Disclose)` plus
    an extra condition `!C(Notify)` (or an assumption pinning `Notify` absent).

It is essentially a small satisfiability / abduction search.  The search space is
not arbitrary boolean assignments: only atoms that appear as **plain literals in
some rule antecedent** can change which rules fire, so those are the *abducible*
facts.  The result is the set of subset-**minimal** fact configurations — the
least you must assert — which keeps the answer small even when many supersets
also work.
-/

/-- A condition the resulting extension must satisfy.
`holds = true`  → the tag `±∂_modality lit` must be present in the derivation;
`holds = false` → it must be absent. -/
structure Condition where
  holds    : Bool
  positive : Bool
  modality : Modality
  lit      : Lit
  deriving Repr, BEq

instance : ToString Condition where
  toString c :=
    let sign := if c.positive then "+∂" else "-∂"
    let body := s!"{sign}_{c.modality} {c.lit}"
    if c.holds then body else s!"¬({body})"

/-- A fact configuration: the literals asserted as facts in a candidate world. -/
abbrev Config := List Lit

/-- How an atom is pinned by the user before search. -/
inductive Assumption where
  | factPos : Atom → Assumption   -- atom is asserted true   (token `a`)
  | factNeg : Atom → Assumption   -- atom is asserted false  (token `~a`)
  | absent  : Atom → Assumption   -- atom may not be a fact  (token `-a`)
  deriving Repr, BEq

def Assumption.atom : Assumption → Atom
  | .factPos a => a
  | .factNeg a => a
  | .absent  a => a

/-- The literal an assumption forces into the facts, if any. -/
def Assumption.forcedLit : Assumption → Option Lit
  | .factPos a => some (.pos a)
  | .factNeg a => some (.neg a)
  | .absent  _ => none

-- ── Goal / assumption parsing ─────────────────────────────────────────────────

private def trimS (s : String) : String := s.trimAscii.toString

private def litOfString (s : String) : Except String Lit :=
  if s.startsWith "~" then
    let a := (s.drop 1).toString
    if a.isEmpty then .error "empty atom after '~'" else .ok (.neg a)
  else if s.isEmpty then .error "empty literal"
  else .ok (.pos s)

/-- Parse a goal/condition token.

Accepted forms (optional leading `!` means "must NOT hold"):
  `O(x)` `F(x)` `P(x)` `Ps(x)` `Pw(x)` `C(x)`   — modal status of `x`
  `x` / `~x`                                     — `x` holds as a (derived) fact, i.e. `C(x)` / `C(~x)`
`F(x)` is sugar for `O(~x)`. Atoms inside may themselves be negated, e.g. `O(~use)`. -/
def parseCondition (raw : String) : Except String Condition := do
  let s0 := trimS raw
  let (holds, s) := if s0.startsWith "!" then (false, trimS (s0.drop 1).toString) else (true, s0)
  if s.isEmpty then .error "empty condition"
  let prefixes := [("Ps(", Modality.Ps, false), ("Pw(", .Pw, false),
                   ("O(", .O, false), ("F(", .O, true),
                   ("P(", .P, false), ("C(", .C, false)]
  match prefixes.find? (fun (p, _, _) => s.startsWith p) with
  | some (p, mod, isF) =>
    if !s.endsWith ")" then .error s!"missing ')' in '{raw}'"
    let inner := trimS ((s.drop p.length).dropEnd 1).toString
    let lit ← litOfString inner
    .ok ⟨holds, true, mod, if isF then lit.compl else lit⟩
  | none =>
    if s.any (fun c => c == '(' || c == ')') then
      .error s!"unknown modal operator in '{raw}' (expected O/F/P/Ps/Pw/C)"
    let lit ← litOfString s
    .ok ⟨holds, true, .C, lit⟩

/-- Parse an assumption token: `a` (true), `~a` (false), or `-a` (must stay absent). -/
def parseAssumption (raw : String) : Except String Assumption := do
  let s := trimS raw
  if s.isEmpty then .error "empty assumption"
  if s.startsWith "-" then
    let a := trimS (s.drop 1).toString
    if a.isEmpty then .error "empty atom after '-'" else .ok (.absent a)
  else match ← litOfString s with
    | .pos a => .ok (.factPos a)
    | .neg a => .ok (.factNeg a)

-- ── Abducible facts ────────────────────────────────────────────────────────────

/-- Plain literals that occur in some rule antecedent (deontic antecedents are
satisfied by the derivation, not by facts, so they are not abducible). -/
def Theory.plainAntecedentLits (thy : Theory) : List Lit :=
  (thy.rules.flatMap fun r =>
    r.antecedent.filterMap fun
      | .plain l   => some l
      | .deontic _ => none).eraseDups

/-- Atoms whose presence/absence as a fact can change which rules fire. -/
def Theory.abducibleAtoms (thy : Theory) : List Atom :=
  (thy.plainAntecedentLits.map (·.atom)).eraseDups

/-- The fact-literals worth trying for `a`: only the polarities actually tested
in some antecedent (so we never assert a literal no rule reads). -/
def Theory.testedLits (thy : Theory) (a : Atom) : List Lit :=
  thy.plainAntecedentLits.filter (·.atom == a)

-- ── Configuration enumeration ──────────────────────────────────────────────────

/-- Cartesian product of per-atom choices, bounded by `cap` configurations.
Each group is `none` (atom absent) plus one `some lit` per tested polarity. -/
private def enumConfigs (groups : List (List (Option Lit))) (cap : Nat) : List Config :=
  groups.foldl (fun acc opts =>
    (acc.flatMap fun cfg => opts.map fun
      | none   => cfg
      | some l => cfg ++ [l]).take cap) [[]]

-- ── Set helpers on configs ─────────────────────────────────────────────────────

private def isSubset (a b : Config) : Bool := a.all (b.contains ·)
private def configEq (a b : Config) : Bool := isSubset a b && isSubset b a

private def dedupConfigs (cs : List Config) : List Config :=
  cs.foldl (fun acc c => if acc.any (configEq c) then acc else acc ++ [c]) []

/-- Keep only configurations with no satisfying proper subset. -/
private def minimalConfigs (sols : List Config) : List Config :=
  sols.filter fun c => !sols.any fun d => !configEq d c && isSubset d c

private def bySize (cs : List Config) : List Config :=
  (cs.toArray.qsort (·.length < ·.length)).toList

-- ── The search ──────────────────────────────────────────────────────────────────

def satisfies (ext : Extension) (conds : List Condition) : Bool :=
  conds.all fun c =>
    let present := ext.derivation.has ⟨c.positive, c.modality, c.lit⟩
    if c.holds then present else !present

structure AbduceResult where
  conds      : List Condition
  forced     : Config            -- literals pinned by assumptions
  minimal    : List Config       -- subset-minimal satisfying configurations
  satisfying : Nat               -- total satisfying configs among those evaluated
  evaluated  : Nat               -- configurations actually tested
  truncated  : Bool              -- search space exceeded `cap`
  cap        : Nat

-- TODO: This could be very slow, need to check this.
/-- Find subset-minimal fact configurations making every condition hold.
`assumptions` pin atoms (and shrink the search space); the theory's own `facts`
line is ignored — facts are exactly what we are solving for. -/
def abduce (thy : Theory) (assumptions : List Assumption) (conds : List Condition)
    (cap : Nat := 20000) : AbduceResult :=
  let forced := assumptions.filterMap (·.forcedLit)
  let pinned := assumptions.map (·.atom)
  let free   := thy.abducibleAtoms.filter (!pinned.contains ·)
  let groups : List (List (Option Lit)) :=
    free.map fun a => none :: (thy.testedLits a).map some
  let spaceSize := groups.foldl (fun n opts => n * opts.length) 1
  let configs := (enumConfigs groups cap).map (forced ++ ·)
  let sols := configs.filter fun cfg =>
    satisfies (computeExtension { thy with facts := cfg }) conds
  let sols := dedupConfigs sols
  let minimal := bySize (minimalConfigs sols)
  { conds, forced, minimal,
    satisfying := sols.length,
    evaluated  := configs.length,
    truncated  := spaceSize > cap,
    cap }

end Deontic
