/-
The inference engine: computes the extension `E(D)` of a defeasible theory.

Implements Governatori (2018) pp.18-21: the constitutive tag ±dC, the
prescriptive obligation/permission tags ±dO, ±dPs, ±dPw, ±dP over
otimes compensation chains, and the non-compliance tag ±d⊥.

This mirrors the Python reference engine (`src/ddl/engine.py`) method-for-method.
Faithful-but-pragmatic choices preserved from there:

* Violation: `violated(c) ⇔ ~c ∈ F` (the opposite was brought about), the
  operative reading of the paper's test that reproduces the worked examples.
* Plain-literal body conditions use `+dC`/`-dC` (which subsume facts) so that
  constitutive rules chain, rather than the paper's literal `l ∈ F`.
* A monotone fixpoint: inner saturation of every ± proof condition, a
  constitutive well-foundedness closure for positive cycles, then a safety net
  tagging anything still undecided negatively.
-/
import Ddl.Syntax
import Ddl.Proof

namespace Ddl

/-- The set of derivable tagged literals, with justifications. Insertion order
is preserved (justifications are appended). -/
structure Extension where
  proven : List Justification := []
deriving Inhabited

namespace Extension

def has (e : Extension) (sign mod : String) (l : Literal) : Bool :=
  e.proven.any (fun j => j.conclusion == { sign := sign, modality := mod, literal := l })

/-- Add a justification unless its conclusion is already proven. Returns the
new extension and whether it actually changed. -/
def add (e : Extension) (j : Justification) : Extension × Bool :=
  if e.proven.any (fun x => x.conclusion == j.conclusion) then (e, false)
  else ({ proven := e.proven ++ [j] }, true)

def justification? (e : Extension) (c : Conclusion) : Option Justification :=
  e.proven.find? (fun j => j.conclusion == c)

def conclusions (e : Extension) (sign : Option String := none) : List Conclusion :=
  (e.proven.filter (fun j => match sign with | some s => j.conclusion.sign == s | none => true)).map (·.conclusion)

-- convenience queries
def provable (e : Extension) (l : Literal) : Bool := e.has "+" "C" l
def refuted (e : Extension) (l : Literal) : Bool := e.has "-" "C" l
def obligation (e : Extension) (l : Literal) : Bool := e.has "+" "O" l
def forbidden (e : Extension) (l : Literal) : Bool := e.has "+" "O" l.complement
def permitted (e : Extension) (l : Literal) : Bool := e.has "+" "P" l
def strongPermitted (e : Extension) (l : Literal) : Bool := e.has "+" "Ps" l
def weakPermitted (e : Extension) (l : Literal) : Bool := e.has "+" "Pw" l
def noncompliant (e : Extension) : Bool := e.has "+" "⊥" BOTTOM

end Extension

/-- `(rule, index)` pairs where `l` is an obligation-head literal of the rule. -/
def occurrences (t : Theory) (l : Literal) : List (Rule × Nat) := Id.run do
  let mut out : List (Rule × Nat) := []
  for r in t.rules do
    if r.mode == "O" then
      let idxs := List.range r.head.length
      for k in idxs do
        match r.head[k]? with
        | some h => if h == l then out := out ++ [(r, k)]
        | none => pure ()
    else if r.mode == "C" && r.head == [l] then
      out := out ++ [(r, 0)]
  return out

def supportsC (t : Theory) (l : Literal) : List Rule :=
  t.rules.filter (fun r => r.mode == "C" && !r.isDefeater && r.head == [l])

def headC (t : Theory) (l : Literal) : List Rule :=
  t.rules.filter (fun r => r.mode == "C" && r.head == [l])

def supportsO (t : Theory) (l : Literal) : List (Rule × Nat) :=
  (occurrences t l).filter (fun ri => !ri.1.isDefeater)

def defeatersO (t : Theory) (l : Literal) : List (Rule × Nat) :=
  (occurrences t l).filter (fun ri => ri.1.isDefeater)

-- ===================================================== body evaluation
def elemApplicable (e : Extension) (b : BodyElem) : Bool :=
  match b with
  | .modal m => e.has (if m.neg then "-" else "+") m.op m.lit
  | .plain l => if isBottom l then e.has "+" "⊥" BOTTOM else e.provable l

def elemDiscarded (e : Extension) (b : BodyElem) : Bool :=
  match b with
  | .modal m => e.has (if m.neg then "+" else "-") m.op m.lit
  | .plain l => if isBottom l then e.has "-" "⊥" BOTTOM else e.refuted l

def bodyApplicable (e : Extension) (r : Rule) : Bool := r.body.all (elemApplicable e)
def bodyDiscarded (e : Extension) (r : Rule) : Bool := r.body.any (elemDiscarded e)

def isModalElem : BodyElem → Bool
  | .modal _ => true
  | .plain _ => false

def bodyPApplicable (e : Extension) (r : Rule) : Bool :=
  if r.mode == "O" then bodyApplicable e r
  else
    if r.body.isEmpty || r.body.any isModalElem then false
    else r.body.all (fun b => e.has "+" "O" b.lit)

def bodyPDiscarded (e : Extension) (r : Rule) : Bool :=
  if r.mode == "O" then bodyDiscarded e r
  else
    if r.body.isEmpty || r.body.any isModalElem then true
    else r.body.any (fun b => e.has "-" "O" b.lit)

/-- The obligation `O c` is violated iff the opposite was brought about. Facts
are fixed, so this is stable. -/
def violated (t : Theory) (c : Literal) : Bool := t.facts.contains c.complement

/-- Rule is applicable for its head literal at `index`: body-p-applicable and
every prior chain obligation is in force and violated. -/
def applicableAt (t : Theory) (e : Extension) (r : Rule) (index : Nat) : Bool :=
  if !bodyPApplicable e r then false
  else (List.range index).all (fun k =>
    match r.head[k]? with
    | some ck => e.has "+" "O" ck && violated t ck
    | none => true)

/-- Stable negation of applicable-at: body provably discarded, or a prior chain
obligation is refuted or not violated. -/
def discardedAt (t : Theory) (e : Extension) (r : Rule) (index : Nat) : Bool :=
  if bodyPDiscarded e r then true
  else (List.range index).any (fun k =>
    match r.head[k]? with
    | some ck => e.has "-" "O" ck || !(violated t ck)
    | none => false)

-- ===================================================== +/- dC
def checkCountersC (t : Theory) (e : Extension) (l : Literal)
    (winners : List Rule) : Option (List (String × String)) := Id.run do
  let mut defeated : List (String × String) := []
  for s in headC t l.complement do
    if bodyDiscarded e s then
      defeated := defeated ++ [(s.label, "discarded (a premise is refuted)")]
    else
      match winners.find? (fun tt => t.beats tt.label s.label) with
      | some beater => defeated := defeated ++ [(s.label, s!"defeated by superior rule {beater.label}")]
      | none => return none
  return some defeated

def tryPlusDC (t : Theory) (e : Extension) (l : Literal) : Option Justification :=
  if t.facts.contains l then
    some { conclusion := ⟨"+", "C", l⟩, kind := "fact" }
  else if t.facts.contains l.complement then none
  else
    let winners := (supportsC t l).filter (bodyApplicable e)
    if winners.isEmpty then none
    else match checkCountersC t e l winners with
      | none => none
      | some defeated =>
        some { conclusion := ⟨"+", "C", l⟩, kind := "rule",
               applied := some winners.head!.label, defeated := defeated }

def tryMinusDC (t : Theory) (e : Extension) (l : Literal) : Option Justification :=
  if t.facts.contains l then none
  else if t.facts.contains l.complement then
    some { conclusion := ⟨"-", "C", l⟩, kind := "refuted",
           detail := s!"complement {l.complement} is a fact" }
  else
    let supports := supportsC t l
    if supports.all (bodyDiscarded e) then
      some { conclusion := ⟨"-", "C", l⟩, kind := "refuted", detail := "no applicable supporting rule" }
    else match (headC t l.complement).find? (fun s =>
            !(bodyDiscarded e s) && bodyApplicable e s &&
            supports.all (fun tt => bodyDiscarded e tt || !(t.beats tt.label s.label))) with
      | some s => some { conclusion := ⟨"-", "C", l⟩, kind := "refuted",
                         defeated := [(s.label, "undefeated counter-rule")] }
      | none => none

-- ===================================================== +/- dO
/-- +dO/+dPs condition 2: every counter-rule applicable for ~q is beaten by a
rule applicable for q. Returns (ok, defeated-trace). -/
def teamHandlesAttackers (t : Theory) (e : Extension) (q : Literal) : Bool × List (String × String) := Id.run do
  let mut defeated : List (String × String) := []
  for sj in occurrences t q.complement do
    let s := sj.1
    if discardedAt t e s sj.2 then
      pure ()
    else
      match (occurrences t q).find? (fun tk => applicableAt t e tk.1 tk.2 && t.beats tk.1.label s.label) with
      | some beater => defeated := defeated ++ [(s.label, s!"defeated by superior rule {beater.1.label}")]
      | none => return (false, defeated)
  return (true, defeated)

def tryPlusDO (t : Theory) (e : Extension) (q : Literal) : Option Justification :=
  let winners := (supportsO t q).filter (fun ri => applicableAt t e ri.1 ri.2)
  if winners.isEmpty then none
  else
    let (ok, defeated) := teamHandlesAttackers t e q
    if !ok then none
    else some { conclusion := ⟨"+", "O", q⟩, kind := "obligation",
                applied := some winners.head!.1.label, defeated := defeated }

def tryMinusDO (t : Theory) (e : Extension) (q : Literal) : Option Justification :=
  let supports := supportsO t q
  if supports.all (fun ri => discardedAt t e ri.1 ri.2) then
    some { conclusion := ⟨"-", "O", q⟩, kind := "refuted", detail := "no applicable obligation rule" }
  else match (occurrences t q.complement).find? (fun sj =>
          applicableAt t e sj.1 sj.2 &&
          (occurrences t q).all (fun tk => discardedAt t e tk.1 tk.2 || !(t.beats tk.1.label sj.1.label))) with
    | some s => some { conclusion := ⟨"-", "O", q⟩, kind := "refuted",
                       defeated := [(s.1.label, "undefeated counter-obligation")] }
    | none => none

-- ===================================================== +/- dPs (strong)
def tryPlusDPs (t : Theory) (e : Extension) (q : Literal) : Option Justification :=
  if e.has "+" "O" q then
    some { conclusion := ⟨"+", "Ps", q⟩, kind := "from-obligation",
           detail := "O q entails strong permission (Prop. 1.6)" }
  else
    let defs := (defeatersO t q).filterMap (fun ri => if bodyPApplicable e ri.1 then some ri.1 else none)
    if defs.isEmpty then none
    else
      let (ok, defeated) := teamHandlesAttackers t e q
      if !ok then none
      else some { conclusion := ⟨"+", "Ps", q⟩, kind := "strong-permission",
                  applied := some defs.head!.label, defeated := defeated }

def tryMinusDPs (t : Theory) (e : Extension) (q : Literal) : Option Justification :=
  if !(e.has "-" "O" q) then none
  else
    let defs := defeatersO t q
    if defs.all (fun ri => bodyPDiscarded e ri.1) then
      some { conclusion := ⟨"-", "Ps", q⟩, kind := "refuted",
             detail := "-dO q and no applicable permissive defeater" }
    else match (occurrences t q.complement).find? (fun sj =>
            applicableAt t e sj.1 sj.2 &&
            (occurrences t q).all (fun tk => discardedAt t e tk.1 tk.2 || !(t.beats tk.1.label sj.1.label))) with
      | some s => some { conclusion := ⟨"-", "Ps", q⟩, kind := "refuted",
                         defeated := [(s.1.label, "undefeated counter-rule")] }
      | none => none

-- ===================================================== +/- dPw (weak)
def tryPlusDPw (_t : Theory) (e : Extension) (q : Literal) : Option Justification :=
  if e.has "-" "O" q.complement then
    some { conclusion := ⟨"+", "Pw", q⟩, kind := "weak-permission",
           detail := s!"the obligation to the contrary (O {q.complement}) is refuted" }
  else none

def tryMinusDPw (_t : Theory) (e : Extension) (q : Literal) : Option Justification :=
  if e.has "+" "O" q.complement then
    some { conclusion := ⟨"-", "Pw", q⟩, kind := "refuted",
           detail := s!"O {q.complement} holds, so q is not weakly permitted" }
  else none

-- ===================================================== +/- dP (generic)
def tryPlusDP (_t : Theory) (e : Extension) (q : Literal) : Option Justification :=
  if e.has "+" "Ps" q then
    some { conclusion := ⟨"+", "P", q⟩, kind := "permission", detail := "holds via Ps" }
  else if e.has "+" "Pw" q then
    some { conclusion := ⟨"+", "P", q⟩, kind := "permission", detail := "holds via Pw" }
  else none

def tryMinusDP (_t : Theory) (e : Extension) (q : Literal) : Option Justification :=
  if e.has "-" "Ps" q && e.has "-" "Pw" q then
    some { conclusion := ⟨"-", "P", q⟩, kind := "refuted", detail := "neither strong nor weak permission holds" }
  else none

-- ===================================================== +/- d⊥
def tryPlusBottom (t : Theory) (e : Extension) : Option Justification :=
  match t.rules.find? (fun r =>
      !r.isDefeater && bodyPApplicable e r && !r.head.isEmpty &&
      r.head.all (fun c => e.has "+" "O" c && violated t c)) with
  | some r => some { conclusion := ⟨"+", "⊥", BOTTOM⟩, kind := "non-compensable",
                     applied := some r.label,
                     detail := "every obligation in the chain is in force and violated" }
  | none => none

def chainCannotTrigger (t : Theory) (e : Extension) (r : Rule) : Bool :=
  if bodyPDiscarded e r || r.head.isEmpty then true
  else r.head.any (fun c => e.has "-" "O" c || !(violated t c))

def tryMinusBottom (t : Theory) (e : Extension) : Option Justification :=
  if (t.rules.filter (fun r => !r.isDefeater)).all (fun r => chainCannotTrigger t e r) then
    some { conclusion := ⟨"-", "⊥", BOTTOM⟩, kind := "refuted",
           detail := "no rule has a fully in-force, fully violated obligation chain" }
  else none

-- ===================================================== support closure (C)
def supportPass (t : Theory) (e : Extension) (S : List Literal) : List Literal × Bool := Id.run do
  let mut S := S
  let mut changed := false
  for r in t.rules do
    if r.mode != "C" || r.isDefeater || r.head.length != 1 then
      pure ()
    else
      let h := r.head.head!
      if S.contains h then
        pure ()
      else if t.facts.contains h.complement && !(t.facts.contains h) then
        pure ()
      else if r.body.any (elemDiscarded e) then
        pure ()
      else
        let allOk := r.body.all (fun b =>
          match b with
          | .plain l => if isBottom l then elemApplicable e b else S.contains l
          | .modal _ => elemApplicable e b)
        if allOk then
          S := S ++ [h]
          changed := true
  return (S, changed)

partial def supportSetCFrom (t : Theory) (e : Extension) (S : List Literal) : List Literal :=
  let (S', ch) := supportPass t e S
  if ch then supportSetCFrom t e S' else S'

def supportSetC (t : Theory) (e : Extension) : List Literal := supportSetCFrom t e t.facts

-- ===================================================== main loop
def applyTagsForLiteral (t : Theory) (l : Literal) (e0 : Extension) : Extension × Bool :=
  let go (st : Extension × Bool) (j? : Option Justification) : Extension × Bool :=
    match j? with
    | some j => let (e', c) := st.1.add j; (e', st.2 || c)
    | none => st
  let st := (e0, false)
  let st := go st (tryPlusDC t st.1 l)
  let st := go st (tryPlusDO t st.1 l)
  let st := go st (tryPlusDPs t st.1 l)
  let st := go st (tryPlusDPw t st.1 l)
  let st := go st (tryPlusDP t st.1 l)
  let st := go st (tryMinusDC t st.1 l)
  let st := go st (tryMinusDO t st.1 l)
  let st := go st (tryMinusDPs t st.1 l)
  let st := go st (tryMinusDPw t st.1 l)
  let st := go st (tryMinusDP t st.1 l)
  st

def innerPass (t : Theory) (hb : List Literal) (e0 : Extension) : Extension × Bool := Id.run do
  let mut e := e0
  let mut ch := false
  for l in hb do
    let (e', c) := applyTagsForLiteral t l e
    e := e'
    ch := ch || c
  match tryPlusBottom t e with
  | some j => let (e', c) := e.add j; e := e'; ch := ch || c
  | none => pure ()
  match tryMinusBottom t e with
  | some j => let (e', c) := e.add j; e := e'; ch := ch || c
  | none => pure ()
  return (e, ch)

partial def innerSaturate (t : Theory) (hb : List Literal) (e : Extension) : Extension :=
  let (e', ch) := innerPass t hb e
  if ch then innerSaturate t hb e' else e'

def supportClosureStep (t : Theory) (hb : List Literal) (e0 : Extension) : Extension × Bool := Id.run do
  let S := supportSetC t e0
  let mut e := e0
  let mut ch := false
  for l in hb do
    if !(e.has "+" "C" l) && !(e.has "-" "C" l) && !(S.contains l) then
      let (e', c) := e.add { conclusion := ⟨"-", "C", l⟩, kind := "refuted",
                             detail := "unsupported (no constructive derivation)" }
      e := e'
      ch := ch || c
  return (e, ch)

partial def outerLoop (t : Theory) (hb : List Literal) (e0 : Extension) : Extension :=
  let e := innerSaturate t hb e0
  let (e, ch) := supportClosureStep t hb e
  if ch then outerLoop t hb e else e

def herbrandLiterals (t : Theory) : List Literal := Id.run do
  let atoms := t.herbrandAtoms.filter (· != BOTTOM_ATOM)
  let sorted := (atoms.toArray.qsort (fun a b => compare a b == Ordering.lt)).toList
  let mut out : List Literal := []
  for a in sorted do
    out := out ++ [{ atom := a, neg := false }, { atom := a, neg := true }]
  return out

def compute (t : Theory) : Extension := Id.run do
  let hb := herbrandLiterals t
  let mut e := outerLoop t hb {}
  -- safety net for any tag still undecided
  for l in hb do
    for mod in MODALITIES do
      if !(e.has "+" mod l) && !(e.has "-" mod l) then
        e := (e.add { conclusion := ⟨"-", mod, l⟩, kind := "refuted",
                      detail := "undecided at fixpoint (not provable)" }).1
  if !(e.has "+" "⊥" BOTTOM) && !(e.has "-" "⊥" BOTTOM) then
    e := (e.add { conclusion := ⟨"-", "⊥", BOTTOM⟩, kind := "refuted",
                  detail := "undecided at fixpoint (compliant)" }).1
  return e

def extension (t : Theory) : Extension := compute t

end Ddl
