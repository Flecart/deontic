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
structure TaggedLit where
  positive : Bool      -- true = +∂, false = −∂
  modality : Modality
  lit      : Lit
  deriving BEq, Repr

instance : ToString TaggedLit where
  toString tl :=
    let sign := if tl.positive then "+∂" else "-∂"
    s!"{sign}_{tl.modality} {tl.lit}"

-- A derivation: finite sequence of tagged literals (§3.1)
abbrev Derivation := Array TaggedLit

def Derivation.has (d : Derivation) (tl : TaggedLit) : Bool :=
  d.any (· == tl)

def Derivation.hasPositive (d : Derivation) (mod : Modality) (l : Lit) : Bool :=
  d.has ⟨true, mod, l⟩

def Derivation.hasNegative (d : Derivation) (mod : Modality) (l : Lit) : Bool :=
  d.has ⟨false, mod, l⟩

-- Extension result: the full derivation plus a flag for non-compensable violation
structure Extension where
  derivation  : Derivation
  hasViolation : Bool   -- +∂_⊥

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
