import Deontic.Theory
import Deontic.ProofTags
import Deontic.Extension

namespace Deontic

-- ── Why: proof certificate for an atom's obligation status ──────────────────

/-- One applicable rule in a why-report, annotated with the labels of the
applicable counter-rules that defeat it by superiority. -/
structure WhyRuleEntry where
  rule       : Rule
  defeatedBy : List String
  deriving Repr

/-- Proof certificate for one atom in one bearer's slice: the status plus the
applicable prescriptive rules on each side of the obligation question
(`forO` concludes the atom, `againstO` its complement). Inapplicable rules are
omitted — they played no part. Defeaters are listed (they attack a side even
though they cannot positively support an obligation). -/
structure WhyReport where
  atom     : Atom
  bearer   : Option String
  status   : String
  forO     : List WhyRuleEntry
  againstO : List WhyRuleEntry
  deriving Repr

/-- Applicable prescriptive rules concluding `q` (at `q`'s position in the
compensatory chain), judged against bearer-scoped theory and derivation. -/
private def applicableRulesConcluding (sthy : Theory) (sv : Derivation)
    (q : Lit) : List Rule :=
  sthy.prescriptiveRules.filter fun r =>
    match r.conclusion.findIdx? (· == q) with
    | some j => applicableForIndex r q j sv sthy.facts
    | none   => false

-- Run extension and filter all tags for a specific atom
def queryAtom (thy : Theory) (a : Atom) : Extension × List TaggedLit :=
  let ext := computeExtension thy
  (ext, ext.tagsFor a)

-- Run extension and check a specific tagged literal
def queryTagged (thy : Theory) (tl : TaggedLit) : Extension × Bool :=
  let ext := computeExtension thy
  (ext, ext.derivation.has tl)

def Extension.isUnresolvedAtomForBearer (ext : Extension) (a : Atom)
    (b : Option String) : Bool :=
  ext.unresolvedConflicts.any fun c => c.atom == a && c.bearer == b

/-- Normative verdict for one bearer slice on atom `a`. Constitutive facts are
shared; deontic tags are read only from `b`'s slice (`none` = unattributed). -/
def normativeStatusForBearer (ext : Extension) (a : Atom) (b : Option String) : String :=
  let pos := Lit.pos a
  let neg := Lit.neg a
  let d := ext.derivation
  if ext.isUnresolvedAtomForBearer a b then "unresolved"
  else if d.hasPositiveForBearer b .O pos then s!"O({a})"
  else if d.hasPositiveForBearer b .O neg then s!"F({a})"
  else if d.hasPositiveForBearer b .Ps pos then s!"Ps({a})"
  else if d.hasPositiveForBearer b .C pos then s!"fact({a})"
  else if d.hasPositiveForBearer b .C neg then s!"fact(~{a})"
  else if d.hasPositiveForBearer b .P pos then s!"P({a})"
  else if d.hasPositiveForBearer b .Pw pos then s!"Pw({a})"
  else "unknown"

def actForbiddenForBearer (ext : Extension) (q : Lit) (b : Option String) : Bool :=
  let d := ext.derivation
  d.hasPositiveForBearer b .O q || d.hasPositiveForBearer b .O q.compl

def actForbiddenAggregate (ext : Extension) (q : Lit) : Bool :=
  ext.derivation.hasPositiveAny .O q || ext.derivation.hasPositiveAny .O q.compl

-- Summarise normative status of an atom as a short string (aggregate view).
def normativeStatus (ext : Extension) (a : Atom) : String :=
  let pos := Lit.pos a
  let neg := Lit.neg a
  if      ext.isUnresolvedAtom a then "unresolved"
  else if ext.derivation.hasPositiveAny .O  pos then s!"O({a})"
  else if ext.derivation.hasPositiveAny .O  neg then s!"F({a})"
  else if ext.derivation.hasPositiveAny .Ps pos then s!"Ps({a})"
  else if ext.derivation.hasPositiveAny .C  pos then s!"fact({a})"
  else if ext.derivation.hasPositiveAny .C  neg then s!"fact(~{a})"
  else if ext.derivation.hasPositiveAny .P  pos then s!"P({a})"
  else if ext.derivation.hasPositiveAny .Pw pos then s!"Pw({a})"
  else "unknown"

/-- Why-report for atom `a` in bearer `b`'s slice. Reuses the same scoping as
the fixed point (`scopedForBearer` / `scopeForBearer`), so the report shows
exactly the rules the proof conditions consulted. -/
def whyForBearer (thy : Theory) (ext : Extension) (a : Atom)
    (b : Option String) : WhyReport :=
  let sthy := thy.scopedForBearer b
  let sv   := ext.derivation.scopeForBearer b
  let pos  := Lit.pos a
  let forR := applicableRulesConcluding sthy sv pos
  let agR  := applicableRulesConcluding sthy sv pos.compl
  let annotate (own opp : List Rule) : List WhyRuleEntry :=
    own.map fun s =>
      { rule := s
        defeatedBy := opp.filterMap fun t =>
          if thy.defeats t.label s.label then some t.label else none }
  { atom := a, bearer := b
    status := normativeStatusForBearer ext a b
    forO := annotate forR agR, againstO := annotate agR forR }

end Deontic
