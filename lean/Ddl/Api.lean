/-
High-level library facade: load a theory, ask a tagged-literal query, get a
verdict with a natural-language proof trace. Port of `src/ddl/api.py`.

The LLM formalises norms (via JSON or DSL), the engine reasons deterministically,
and the verdict + trace are handed back for the LLM to verbalise.
-/
import Ddl.Engine
import Ddl.Parser
import Ddl.Render

namespace Ddl

private def bottomPos : List String :=
  ["+d_bottom", "+dbottom", "+d⊥", "bottom", "noncompliant", "non-compliant"]
private def bottomNeg : List String := ["-d_bottom", "-dbottom", "-d⊥", "compliant"]

/-- True if the modality holds vacuously for a literal outside the Herbrand
base (Pw / generic P hold in the absence of any prohibition). -/
def vacuousPos (mod : String) : Bool := mod == "Pw" || mod == "P"

private def matchModality (s : String) (ops : List String) : Option (String × String) :=
  ops.findSome? (fun op =>
    if s.startsWith op then
      let after := sdrop s op.length
      if after.length > 0 && (sfront after).isWhitespace then some (op, trim after) else none
    else none)

private def matchTag (t : String) : Option Conclusion :=
  let (sign, afterSign) :=
    if t.startsWith "+" then ("+", sdrop t 1)
    else if t.startsWith "-" then ("-", sdrop t 1)
    else ("+", t)
  if afterSign.startsWith "d" then
    match matchModality (sdrop afterSign 1) ["C", "O", "Ps", "Pw", "P"] with
    | some (mod, rest) => (parseLiteralStr rest).toOption.map (fun l => ⟨sign, mod, l⟩)
    | none => none
  else none

private def matchFriendly (t : String) : Option Conclusion :=
  match matchModality t ["O", "F", "Pw", "Ps", "P"] with
  | some (op, rest) =>
    match (parseLiteralStr rest).toOption with
    | some l =>
      if op == "F" then some ⟨"+", "O", l.complement⟩
      else some ⟨"+", (if op == "O" then "O" else op), l⟩
    | none => none
  | none => none

/-- Parse a query into a target `Conclusion`. Accepts the tag form
(`+dO remove`, `-dC publish`), the friendly form (`O remove`, `F publish`,
`P use`), `bottom`/`compliant`, or a bare literal (`publish` == `+dC publish`). -/
def parseQuery (text : String) : Conclusion :=
  let t := trim text
  let low := t.map Char.toLower
  if bottomPos.contains low then ⟨"+", "⊥", BOTTOM⟩
  else if bottomNeg.contains low then ⟨"-", "⊥", BOTTOM⟩
  else match matchTag t with
    | some c => c
    | none => match matchFriendly t with
      | some c => c
      | none => ⟨"+", "C", (parseLiteralStr t).toOption.getD BOTTOM⟩

structure Verdict where
  conclusion : Conclusion
  holds      : Bool
  summary    : String
  trace      : List String := []

def Verdict.toString (v : Verdict) : String :=
  let head := s!"{if v.holds then "YES" else "NO "} | {v.summary}"
  if v.trace.isEmpty then head else head ++ "\n" ++ String.intercalate "\n" v.trace

instance : ToString Verdict := ⟨Verdict.toString⟩

structure Reasoner where
  theory : Theory
  ext    : Extension

def Reasoner.ofTheory (t : Theory) : Reasoner := { theory := t, ext := extension t }
def Reasoner.fromDdl (src : String) : Except String Reasoner := (parse src).map Reasoner.ofTheory
def Reasoner.withFacts (r : Reasoner) (facts : List Literal) : Reasoner :=
  Reasoner.ofTheory (r.theory.withFacts facts)

private def elemConclusion (b : BodyElem) : Conclusion :=
  match b with
  | .modal m => ⟨if m.neg then "-" else "+", m.op, m.lit⟩
  | .plain l => if isBottom l then ⟨"+", "⊥", BOTTOM⟩ else ⟨"+", "C", l⟩

private def pad (indent : Nat) : String := String.join (List.replicate indent "  ")

partial def traceConcl (r : Reasoner) (c : Conclusion) (visited : List Conclusion) (indent : Nat) : List String :=
  match r.ext.justification? c with
  | none => [s!"{pad indent}- {describeConclusion c} (not derived)"]
  | some j =>
    let head := s!"{pad indent}- {describeConclusion c}  [{j.kind}"
      ++ (match j.applied with | some a => s!" via {a}]" | none => "]")
    let out := [head] ++ j.defeated.map (fun (label, why) => s!"{pad indent}    (counter {label}: {why})")
    if visited.contains c || j.applied.isNone then out
    else
      let visited := visited ++ [c]
      match j.applied.bind r.theory.rule? with
      | none => out
      | some rule => out ++ rule.body.flatMap (fun b => traceConcl r (elemConclusion b) visited (indent + 1))

def Reasoner.query (r : Reasoner) (query : Conclusion) (trace : Bool := true) : Verdict :=
  let inBase := query.modality == "⊥" || r.theory.herbrandAtoms.contains query.literal.atom
  let ok :=
    if inBase then r.ext.proven.any (fun j => j.conclusion == query)
    else if query.positive then vacuousPos query.modality else !(vacuousPos query.modality)
  let summary := describeConclusion ⟨"+", query.modality, query.literal⟩
  let lines := if trace && ok && inBase then traceConcl r query [] 0 else []
  { conclusion := query, holds := ok, summary := summary, trace := lines }

def Reasoner.queryStr (r : Reasoner) (q : String) (trace : Bool := true) : Verdict :=
  r.query (parseQuery q) trace

def Reasoner.holds (r : Reasoner) (q : String) : Bool := (r.queryStr q false).holds

-- ------------------------------------------------------------- reporting
private def modOrder (mod : String) : Nat :=
  match mod with
  | "O" => 0 | "Ps" => 1 | "P" => 2 | "Pw" => 3 | "⊥" => 4 | "C" => 5 | _ => 9
private def conciseMods : List String := ["O", "Ps", "⊥", "C"]

def Reasoner.conclusions (r : Reasoner) (concise : Bool := true) : List Conclusion :=
  let pos := r.ext.conclusions (some "+")
  let filtered := if concise then pos.filter (fun c => conciseMods.contains c.modality) else pos
  let deduped := filtered.foldl (fun acc c => if acc.contains c then acc else acc ++ [c]) []
  -- sort by (modality order, literal string)
  let key := fun (c : Conclusion) => (modOrder c.modality, toString c.literal)
  deduped.toArray.qsort (fun a b =>
    let (o1, s1) := key a; let (o2, s2) := key b
    if o1 != o2 then o1 < o2 else compare s1 s2 == .lt) |>.toList

def Reasoner.report (r : Reasoner) (concise : Bool := true) : String := Id.run do
  let mut lines := ["= Theory =", describeTheory r.theory, "", "= Conclusions ="]
  for c in r.conclusions concise do
    lines := lines ++ [s!"  {c}\t{describeConclusion c}"]
  return String.intercalate "\n" lines

end Ddl
