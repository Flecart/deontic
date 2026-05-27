/-
Abstract syntax for Defeasible Deontic Logic theories.

Follows Governatori (2018), "Practical Normative Reasoning with Defeasible
Deontic Logic". A theory is `D = (F, R^C, R^O, <)` where `F` is a set of plain
literals (facts), `R^C` constitutive rules, `R^O` prescriptive rules, and `<`
the superiority relation.

Design note on the superiority relation: the paper's worked examples are only
consistent if `r < s` means *s is superior* (s defeats r). We store ordered
pairs `(weaker, stronger)`; see `Theory.beats`.

This is a direct port of the Python reference implementation in `src/ddl`.
-/

namespace Ddl

/-- A plain literal: an atom or its negation. -/
structure Literal where
  atom : String
  neg  : Bool := false
deriving BEq, Hashable, Repr, DecidableEq, Inhabited

namespace Literal

def complement (l : Literal) : Literal := { atom := l.atom, neg := !l.neg }

instance : ToString Literal where
  toString l := if l.neg then s!"-{l.atom}" else l.atom

end Literal

/-- The distinguished literal for a non-compensable violation (Governatori 2018,
pp.20-21). It carries the `+d⊥` proof tag and may only appear in rule
antecedents. -/
def BOTTOM_ATOM : String := "⊥"
def BOTTOM : Literal := { atom := BOTTOM_ATOM, neg := false }

def isBottom (l : Literal) : Bool := l.atom == BOTTOM_ATOM

/-- A deontic literal: a deontic operator applied to a plain literal.
`neg` marks the negation of the whole modal literal (e.g. `-Op`). Prohibition
`Fp` is encoded as `ModalLiteral` with op `"O"` and the complement of `p`. -/
structure ModalLiteral where
  op  : String
  lit : Literal
  neg : Bool := false
deriving BEq, Hashable, Repr, DecidableEq, Inhabited

instance : ToString ModalLiteral where
  toString m := (if m.neg then "-" else "") ++ m.op ++ toString m.lit

/-- A rule body element is either a plain literal (a brute fact condition) or a
modal literal (a normative condition that must itself be derived). -/
inductive BodyElem where
  | plain (l : Literal)
  | modal (m : ModalLiteral)
deriving BEq, Repr, DecidableEq, Inhabited

namespace BodyElem

/-- The inner plain literal (used for collecting the Herbrand base). -/
def lit : BodyElem → Literal
  | .plain l => l
  | .modal m => m.lit

instance : ToString BodyElem where
  toString
    | .plain l => toString l
    | .modal m => toString m

end BodyElem

/-- A defeasible rule or defeater.

`mode` distinguishes constitutive (`"C"`, counts-as -> plain conclusion) from
prescriptive (`"O"`, -> obligation). `head` is the consequent as an ordered
list of plain literals: a singleton for constitutive rules, or a compensation
(otimes) chain for prescriptive rules, where `head[0]` is the primary
obligation and later elements are contrary-to-duty compensations. -/
structure Rule where
  label    : String
  mode     : String           -- "C" or "O"
  strength : String           -- "defeasible" or "defeater"
  body     : List BodyElem
  head     : List Literal
  gloss    : String := ""
deriving Repr, Inhabited

namespace Rule

def isDefeater (r : Rule) : Bool := r.strength == "defeater"

def primary (r : Rule) : Literal := r.head.headD BOTTOM

instance : ToString Rule where
  toString r :=
    let arrow := if r.isDefeater then "~>" else "=>"
    let body := String.intercalate ", " (r.body.map toString)
    let head := String.intercalate " (x) " (r.head.map toString)
    s!"{r.label}: {body} {arrow}{r.mode} {head}"

end Rule

/-- A defeasible deontic theory `D = (F, R^C, R^O, <)`. Facts and superiority
are stored as lists (used as sets via membership tests). -/
structure Theory where
  facts       : List Literal := []
  rules       : List Rule := []
  superiority : List (String × String) := []   -- (weaker, stronger): weaker < stronger
deriving Inhabited

namespace Theory

/-- True if rule `stronger` is superior to rule `weaker`. -/
def beats (t : Theory) (stronger weaker : String) : Bool :=
  t.superiority.contains (weaker, stronger)

def constitutive (t : Theory) : List Rule := t.rules.filter (·.mode == "C")
def prescriptive (t : Theory) : List Rule := t.rules.filter (·.mode == "O")

def rule? (t : Theory) (label : String) : Option Rule :=
  t.rules.find? (·.label == label)

def hasFact (t : Theory) (l : Literal) : Bool := t.facts.contains l

/-- A shallow copy with additional facts (for what-if / appeal queries). -/
def withFacts (t : Theory) (extra : List Literal) : Theory :=
  { t with facts := t.facts ++ extra.filter (fun l => !t.facts.contains l) }

def herbrandAtoms (t : Theory) : List String := Id.run do
  let mut atoms : List String := []
  let push (atoms : List String) (a : String) : List String :=
    if atoms.contains a then atoms else atoms ++ [a]
  for f in t.facts do
    atoms := push atoms f.atom
  for r in t.rules do
    for b in r.body do
      atoms := push atoms b.lit.atom
    for h in r.head do
      atoms := push atoms h.atom
  return atoms

end Theory

/-- Apply otimes duplication/contraction (sect. 3.2): keep the leftmost
occurrence of each literal, dropping later duplicates. -/
def normalizeChain (head : List Literal) : List Literal := Id.run do
  let mut seen : List Literal := []
  let mut out : List Literal := []
  for h in head do
    if !seen.contains h then
      seen := seen ++ [h]
      out := out ++ [h]
  return out

def lit (atom : String) (neg : Bool := false) : Literal := { atom := atom, neg := neg }

end Ddl
