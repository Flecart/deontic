import Deontic.Basic

namespace Deontic

-- Modalities □ ∈ {C, O, P, Pw, Ps}  (§3.3 p.17)
inductive Modality where
  | C   -- constitutive / factual
  | O   -- obligation
  | P   -- generic permission
  | Pw  -- weak permission
  | Ps  -- strong permission
  deriving BEq, Repr, Hashable

instance : ToString Modality where
  toString
    | .C  => "C"
    | .O  => "O"
    | .P  => "P"
    | .Pw => "Pw"
    | .Ps => "Ps"

-- A tagged literal: +∂_□ q  or  −∂_□ q
-- `bearer` names the party that bears the obligation/permission (Hohfeldian
-- directedness): a duty is always *someone's* duty. It is `none` for the
-- bearer-neutral constitutive modality `C` and for legacy/unattributed norms
-- (rules written without an `@Party`); `some p` for a directed deontic tag.
-- The bearer lives on the tag, not the atom — the act is shared, the duty is
-- directed (see docs/architecture.md).
structure TaggedLit where
  positive : Bool      -- true = +∂, false = −∂
  modality : Modality
  bearer   : Option String := none
  lit      : Lit
  deriving BEq, Repr

private def bearerSuffix : Option String → String
  | some p => s!"@{p}"
  | none   => ""

instance : ToString TaggedLit where
  toString tl :=
    let sign := if tl.positive then "+∂" else "-∂"
    s!"{sign}_{tl.modality}{bearerSuffix tl.bearer} {tl.lit}"

-- A derivation: finite sequence of tagged literals (§3.1)
abbrev Derivation := Array TaggedLit

def Derivation.has (d : Derivation) (tl : TaggedLit) : Bool :=
  d.any (· == tl)

-- Bearer-neutral membership (bearer = none): the proof conditions in
-- `ProofConditions.lean` run on bearer-scoped *views* of the derivation in which
-- every deontic tag has been collapsed to `bearer = none`, so these helpers keep
-- their original (bearer-blind) signatures and the calculus stays untouched.
def Derivation.hasPositive (d : Derivation) (mod : Modality) (l : Lit) : Bool :=
  d.has ⟨true, mod, none, l⟩

def Derivation.hasNegative (d : Derivation) (mod : Modality) (l : Lit) : Bool :=
  d.has ⟨false, mod, none, l⟩

-- Existential over bearers: "is `l` tagged `+∂_mod` for *some* bearer?" Used for
-- reporting/queries (an atom's status regardless of who bears it).
def Derivation.hasPositiveAny (d : Derivation) (mod : Modality) (l : Lit) : Bool :=
  d.any fun tl => tl.positive && tl.modality == mod && tl.lit == l

-- ── Bearer-scoped views (for the per-bearer fixed point in Extension) ─────────
-- `scopeForBearer b`: the slice of the derivation visible to bearer `b`'s
-- obligation derivation — every constitutive (`C`) tag (bearer-neutral, shared)
-- plus the deontic tags borne by `b`, rebearered to `none` so the unchanged
-- proof conditions can read them with their bearer-blind helpers.
def Derivation.scopeForBearer (d : Derivation) (b : Option String) : Derivation :=
  d.filterMap fun tl =>
    if tl.modality == .C then some tl
    else if tl.bearer == b then some { tl with bearer := none }
    else none

-- `flattenBearers`: the view the bearer-neutral constitutive layer sees — a
-- deontic antecedent like `O(x)` in a constitutive rule holds when *any* party is
-- obliged `x`. Collapses every deontic tag to `bearer = none` and dedups.
def Derivation.flattenBearers (d : Derivation) : Derivation :=
  (d.map fun tl => if tl.modality == .C then tl else { tl with bearer := none })
    |>.foldl (fun acc tl => if acc.has tl then acc else acc.push tl) #[]

-- Applicable rules attack each other on O(a) vs O(~a) but ≺ does not pick a winner.
-- A conflict is per *bearer*: two parties holding opposite duties on the same atom
-- are not in conflict (they are separate norms), so `bearer` records whose duties
-- deadlock (`none` for unattributed rules).
structure UnresolvedConflict where
  atom       : Atom
  forO       : List String   -- rule labels supporting O(atom)
  againstO   : List String   -- rule labels supporting O(~atom)
  pairs      : List (String × String)  -- (r, s) with no r > s nor s > r
  bearer     : Option String := none
  deriving Repr

-- Extension result: the full derivation plus a flag for non-compensable violation
structure Extension where
  derivation  : Derivation
  hasViolation : Bool   -- +∂_⊥
  -- Labels of the rules witnessing +∂_⊥ (their whole conclusion chain is both
  -- obligated and violated, so no compensation remains). Empty iff no violation.
  violatingRuleLabels : List String := []
  unresolvedConflicts : List UnresolvedConflict := []

def Extension.hasUnresolvedConflicts (ext : Extension) : Bool :=
  !ext.unresolvedConflicts.isEmpty

def Extension.isUnresolvedAtom (ext : Extension) (a : Atom) : Bool :=
  ext.unresolvedConflicts.any (·.atom == a)

-- Collect all positive tags for a given atom across all modalities
def Extension.tagsFor (ext : Extension) (a : Atom) : List TaggedLit :=
  ext.derivation.toList.filter fun tl =>
    tl.lit.atom == a && tl.positive

-- The human-readable "verdict" for an atom:
-- returns the strongest positive deontic tag, or "unknown" if none
def Extension.verdict (ext : Extension) (a : Atom) : String :=
  let tags := ext.tagsFor a
  -- priority: O > Ps > P > Pw > C
  let checkMod (m : Modality) : Option String :=
    if tags.any (fun t => t.modality == m) then
      some s!"{m}({a})"
    else none
  checkMod .O
    |>.orElse (fun _ => checkMod .Ps)
    |>.orElse (fun _ => checkMod .P)
    |>.orElse (fun _ => checkMod .Pw)
    |>.orElse (fun _ => checkMod .C)
    |>.getD "unknown"

end Deontic
