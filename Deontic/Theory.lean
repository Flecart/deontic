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
-- A labelled rule. `bearer` names the party that bears a prescriptive rule's
-- obligation/permission (`=>O@Vendor …`); it is `none` for constitutive rules
-- and for unattributed prescriptive rules (`=>O …`, legacy/optional). The bearer
-- rides on the obligation, not the act — see docs/architecture.md.
structure Rule where
  label      : String
  strength   : RuleStrength
  family     : RuleFamily
  antecedent : List Literal
  conclusion : OExpr
  bearer     : Option String := none
  deriving BEq, Repr

-- Superiority relation ≺ ⊆ R×R
-- (winner, loser): winner defeats loser when both are applicable and conflict
abbrev SuperiorityRel := List (String × String)

-- Provenance for an atom: where its meaning comes from. At least one field must
-- be filled (enforced by the parser).
--   quote : a verbatim snapshot of the source text
--   uri   : a relative path to an in-repo markdown source, with an optional
--           GitHub-style line selector (`docs/sources/nda.md#L3-L5`)
-- Both filled is the Ricardian sweet spot: a cached snapshot plus a pointer to
-- where it lives, so drift can be detected later.
structure Provenance where
  quote : Option String := none
  uri   : Option String := none
  deriving Repr, BEq

def Provenance.isEmpty (p : Provenance) : Bool := p.quote.isNone && p.uri.isNone

-- An atom declaration: the human/LLM-facing meaning of an atom plus optional
-- provenance. Descriptions ground the otherwise opaque atom names so a
-- fact-finder (human or LLM) knows what asserting the atom commits to.
structure AtomDecl where
  atom        : Atom
  description : String
  provenance  : Option Provenance := none
  deriving Repr, BEq

-- An import directive (resolved by the loader, not the pure parser).
--   namespaced path alias : `import <path> as <alias>` — imported atoms/labels
--                           are prefixed `alias.` (alias defaults to the file stem)
--   glob path             : `from <path> import *` — merged into this namespace,
--                           with description-guarded conflict checking
inductive ImportDecl where
  | namespaced (path : String) (alias : String)
  | glob       (path : String)
  deriving Repr, BEq

def ImportDecl.path : ImportDecl → String
  | .namespaced p _ => p
  | .glob p         => p

-- Defeasible Deontic Theory D = (F, R^C, R^O, ≺)  eq. 29
structure Theory where
  facts       : List Lit
  rules       : List Rule
  superiority : SuperiorityRel
  atoms       : List AtomDecl   := []
  imports     : List ImportDecl := []

-- ── Helpers ──────────────────────────────────────────────────────────────────

def Theory.constitutiveRules (thy : Theory) : List Rule :=
  thy.rules.filter (·.family == .constitutive)

def Theory.prescriptiveRules (thy : Theory) : List Rule :=
  thy.rules.filter (·.family == .prescriptive)

-- The distinct bearers carried by prescriptive rules (includes `none` if any
-- prescriptive rule is unattributed). The per-bearer fixed point in
-- `Extension.lean` derives obligations/permissions once for each. A theory with
-- no `@`-attributed rules yields `[none]`, reducing to the original calculus.
def Theory.bearers (thy : Theory) : List (Option String) :=
  (thy.prescriptiveRules.map (·.bearer)).eraseDups

-- The theory as seen by bearer `b`'s obligation derivation: all constitutive
-- rules (bearer-neutral, shared) plus the prescriptive rules borne by `b`. Other
-- parties' prescriptive rules are invisible, so a counter-rule of a *different*
-- bearer cannot attack `b`'s obligation (Vendor's O(a) and Customer's O(~a)
-- coexist rather than deadlock).
def Theory.scopedForBearer (thy : Theory) (b : Option String) : Theory :=
  { thy with rules := thy.rules.filter fun r =>
      r.family == .constitutive || r.bearer == b }

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

-- ── Namespacing (for imports) ─────────────────────────────────────────────────
-- Prefix every name in a theory with `ns.` so an imported module's atoms and
-- rule labels don't collide with the importer's. Empty prefix is the identity.

private def qualifyName (ns : String) (name : String) : String :=
  if ns.isEmpty then name else s!"{ns}.{name}"

private def Lit.qualify (ns : String) : Lit → Lit
  | .pos a => .pos (qualifyName ns a)
  | .neg a => .neg (qualifyName ns a)

private def Literal.qualify (ns : String) : Literal → Literal
  | .plain l   => .plain (l.qualify ns)
  | .deontic d => .deontic { d with lit := d.lit.qualify ns }

def Theory.namespaced (ns : String) (thy : Theory) : Theory where
  facts       := thy.facts.map (·.qualify ns)
  rules       := thy.rules.map fun r =>
    { r with label      := qualifyName ns r.label
             antecedent := r.antecedent.map (·.qualify ns)
             conclusion := r.conclusion.map (·.qualify ns) }
  superiority := thy.superiority.map fun (w, l) => (qualifyName ns w, qualifyName ns l)
  atoms       := thy.atoms.map fun d => { d with atom := qualifyName ns d.atom }
  imports     := []

-- Guarded merge: combine `add` into `base`. Two declarations of the same atom
-- must agree on their description (else the atoms aren't really the same thing);
-- two rules may not share a label. This is what makes `from x import *` safe.
def Theory.mergeGuarded (base add : Theory) : Except String Theory := do
  for d in add.atoms do
    match base.atoms.find? (·.atom == d.atom) with
    | some e =>
      if e.description != d.description then
        .error s!"conflicting descriptions for atom '{d.atom}':\n  {e.description}\n  {d.description}"
    | none => pure ()
  for r in add.rules do
    if base.rules.any (·.label == r.label) then
      .error s!"duplicate rule label '{r.label}' across imports"
  .ok {
    facts       := base.facts ++ add.facts
    rules       := base.rules ++ add.rules
    superiority := base.superiority ++ add.superiority
    atoms       := base.atoms ++ add.atoms.filter fun d =>
                     !base.atoms.any (·.atom == d.atom)
    imports     := []
  }

-- The declaration for an atom, if one was provided.
def Theory.atomDecl? (thy : Theory) (a : Atom) : Option AtomDecl :=
  thy.atoms.find? (·.atom == a)

-- Atoms used in the theory that have no description (the checker complains
-- about these: every atom should be grounded so a fact-finder knows its meaning).
def Theory.undescribedAtoms (thy : Theory) : List Atom :=
  thy.herbrandBase.filter fun a => (thy.atomDecl? a).isNone

end Deontic
