/-
Natural-language rendering of theories and conclusions (the audit round-trip).
Lets a human or an LLM verify *"did I formalise this faithfully?"* and read
verdicts back in plain English. Port of `src/ddl/render.py`.
-/
import Ddl.Syntax
import Ddl.Proof

namespace Ddl

def opPhrase (op : String) (inner : String) : String :=
  match op with
  | "O"  => s!"it is obligatory that {inner}"
  | "P"  => s!"it is permitted that {inner}"
  | "Pw" => s!"it is weakly permitted that {inner}"
  | "Ps" => s!"it is strongly permitted that {inner}"
  | _    => s!"{op} {inner}"

def phraseLiteral (l : Literal) : String :=
  if isBottom l then "a non-compensable violation"
  else if l.neg then s!"not {l.atom}" else l.atom

def phraseElem (b : BodyElem) : String :=
  match b with
  | .plain l => phraseLiteral l
  | .modal m =>
    let inner := phraseLiteral m.lit
    let base := if m.op == "O" && m.lit.neg then s!"{m.lit.atom} is forbidden" else opPhrase m.op inner
    if m.neg then s!"it is not the case that {base}" else base

def describeRule (r : Rule) : String :=
  let kind := if r.isDefeater then "defeater" else "rule"
  let family := if r.mode == "C" then "constitutive" else "prescriptive"
  let cond := if r.body.isEmpty then ""
    else s!"if {String.intercalate " and " (r.body.map phraseElem)}, then "
  let headStr :=
    if r.mode == "O" then
      let primary := r.head.headD BOTTOM
      let base := if primary.neg then s!"{primary.atom} is forbidden"
                  else s!"it is obligatory that {primary.atom}"
      match r.head.tail with
      | [] => base
      | comps => base ++ s!" (compensated, in order, by: {String.intercalate ", failing which " (comps.map phraseLiteral)})"
    else s!"it counts as {phraseLiteral (r.head.headD BOTTOM)}"
  s!"{r.label} [{family} {kind}]: {cond}{headStr}"

def describeConclusion (c : Conclusion) : String :=
  if c.modality == "⊥" then
    if c.positive then "the situation is NON-COMPLIANT (a non-compensable violation occurred)"
    else "the situation is compliant (no non-compensable violation)"
  else
    let l := c.literal
    if c.modality == "C" then
      let body := phraseLiteral l
      if c.positive then s!"{body} holds" else s!"{body} is not provable"
    else
      let base :=
        if c.modality == "O" then
          if l.neg then s!"{l.atom} is forbidden (F {l.atom})"
          else s!"{l.atom} is obligatory (O {l.atom})"
        else
          let label := match c.modality with
            | "P"  => "permitted"
            | "Pw" => "weakly permitted"
            | "Ps" => "strongly permitted"
            | _    => c.modality
          s!"{phraseLiteral l} is {label} ({c.modality} {l})"
      if c.positive then base else s!"it is NOT the case that {base}"

def describeTheory (theory : Theory) : String := Id.run do
  let mut lines : List String := []
  if !theory.facts.isEmpty then
    let facts := (theory.facts.map phraseLiteral).toArray.qsort (· < ·) |>.toList
    lines := lines ++ [s!"Facts: {String.intercalate ", " facts}."]
  if !theory.rules.isEmpty then
    lines := lines ++ ["Norms:"]
    for r in theory.rules do
      lines := lines ++ [s!"  - {describeRule r}"]
  if !theory.superiority.isEmpty then
    lines := lines ++ ["Priorities:"]
    let cmpPair := fun (a b : String × String) =>
      if a.1 != b.1 then compare a.1 b.1 == Ordering.lt else compare a.2 b.2 == Ordering.lt
    let sorted := theory.superiority.toArray.qsort cmpPair |>.toList
    for (weaker, stronger) in sorted do
      lines := lines ++ [s!"  - {stronger} overrides {weaker}"]
  return String.intercalate "\n" lines

end Ddl
