import Deontic.Basic

namespace Deontic

-- Three rule strengths from §3.1
inductive RuleStrength where
  | strict     -- ->  : conclusion always follows when premises hold
  | defeasible -- =>  : conclusion holds unless defeated
  | defeater   -- ~>  : blocks conclusions, does not support them
  deriving BEq, Repr

-- Two rule families from §3.3
inductive RuleFamily where
  | constitutive  -- R^C: defines institutional facts from brute facts
  | prescriptive  -- R^O: determines normative effects (obligations)
  deriving BEq, Repr

instance : ToString RuleStrength where
  toString
    | .strict     => "->"
    | .defeasible => "=>"
    | .defeater   => "~>"

instance : ToString RuleFamily where
  toString
    | .constitutive => "C"
    | .prescriptive => "O"

-- A labelled rule  r : a1,...,an ↪ C  (eq. 19 in the paper)
-- For constitutive rules conclusion is a singleton OExpr
-- For prescriptive rules conclusion is an OExpr (possibly a chain)
structure Rule where
  label      : String
  strength   : RuleStrength
  family     : RuleFamily
  antecedent : List Literal
  conclusion : OExpr
  deriving BEq, Repr

-- Superiority relation ≺ ⊆ R×R
-- (winner, loser): winner defeats loser when both are applicable and conflict
abbrev SuperiorityRel := List (String × String)

-- An atom declaration: the human/LLM-facing meaning of an atom plus optional
-- provenance (a URI, a legal citation, or inline source text — see docs).
-- Descriptions ground the otherwise opaque atom names so a fact-finder (human
-- or LLM) knows what asserting the atom commits to.
structure AtomDecl where
  atom        : Atom
  description : String
  provenance  : Option String := none
  deriving Repr, BEq

-- Defeasible Deontic Theory D = (F, R^C, R^O, ≺)  eq. 29
structure Theory where
  facts       : List Lit
  rules       : List Rule
  superiority : SuperiorityRel
  atoms       : List AtomDecl := []

-- ── Helpers ──────────────────────────────────────────────────────────────────

def Theory.constitutiveRules (thy : Theory) : List Rule :=
  thy.rules.filter (·.family == .constitutive)

def Theory.prescriptiveRules (thy : Theory) : List Rule :=
  thy.rules.filter (·.family == .prescriptive)

def Theory.defeatersOf (thy : Theory) : List Rule :=
  thy.rules.filter (·.strength == .defeater)

-- Rules whose conclusion head (first element of OExpr) is the given literal
def Theory.rulesFor (thy : Theory) (q : Lit) : List Rule :=
  thy.rules.filter fun r => r.conclusion.head? == some q

-- Strict-or-defeasible rules for q (excludes defeaters)
def Theory.sdRulesFor (thy : Theory) (q : Lit) : List Rule :=
  thy.rulesFor q |>.filter (·.strength != .defeater)

-- r defeats s: r > s in the superiority relation
def Theory.defeats (thy : Theory) (r s : String) : Bool :=
  thy.superiority.any fun (w, l) => w == r && l == s

-- The Herbrand base: all atoms mentioned anywhere in the theory
def Theory.herbrandBase (thy : Theory) : List Atom :=
  let fromFacts := thy.facts.map (·.atom)
  let fromRules := (thy.rules.flatMap fun r =>
    (r.antecedent.flatMap fun lit =>
      match lit with
      | .plain l  => [l.atom]
      | .deontic d => [d.lit.atom]) ++
    r.conclusion.map (·.atom))
  (fromFacts ++ fromRules).eraseDups

-- The declaration for an atom, if one was provided.
def Theory.atomDecl? (thy : Theory) (a : Atom) : Option AtomDecl :=
  thy.atoms.find? (·.atom == a)

-- Atoms used in the theory that have no description (the checker complains
-- about these: every atom should be grounded so a fact-finder knows its meaning).
def Theory.undescribedAtoms (thy : Theory) : List Atom :=
  thy.herbrandBase.filter fun a => (thy.atomDecl? a).isNone

end Deontic
