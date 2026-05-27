/-
Structured-JSON theory interface -- the LLM-facing front end. Self-documenting
field names instead of the terse DSL operators. The JSON and the `.ddl` DSL
compile to the same `Theory`. Port of `src/ddl/json_io.py`.

Theory shape::

    { "facts": ["license", "publish"],
      "rules": [
        {"id": "r2", "kind": "prescriptive", "strength": "defeasible",
         "if": [], "then": {"obligation": ["-publish", "remove"]}},
        {"id": "c31", "kind": "constitutive",
         "if": ["highSpend"], "then": {"counts_as": "premiumCustomer"}} ],
      "superiority": [["r0", "r1"]] }
-/
import Ddl.Syntax
import Ddl.Parser
import Lean.Data.Json

namespace Ddl
open Lean (Json)

private def optArr (j : Json) (key : String) : Except String (List Json) :=
  match j.getObjVal? key with
  | .ok v => (v.getArr?).map Array.toList
  | .error _ => .ok []

private def optStr (j : Json) (key : String) : Option String :=
  (j.getObjVal? key).toOption.bind (fun v => v.getStr?.toOption)

private def headFromJson (thenJ : Json) (kind : Option String) (label : String) :
    Except String (String × List Literal) := do
  match thenJ.getStr? with
  | .ok s =>
    let mode := if kind == some "prescriptive" then "O" else "C"
    let l ← parseLiteralStr s
    return (mode, [l])
  | .error _ =>
    match thenJ.getObjVal? "obligation" with
    | .ok ob =>
      let chain ← (match ob.getStr? with
        | .ok s => pure [s]
        | .error _ => do let a ← ob.getArr?; a.toList.mapM (fun x => x.getStr?))
      let lits ← chain.mapM parseLiteralStr
      return ("O", normalizeChain lits)
    | .error _ =>
      match thenJ.getObjVal? "forbidden" with
      | .ok fb => do let s ← fb.getStr?; let l ← parseLiteralStr s; return ("O", [l.complement])
      | .error _ =>
        match thenJ.getObjVal? "counts_as" with
        | .ok ca => do let s ← ca.getStr?; let l ← parseLiteralStr s; return ("C", [l])
        | .error _ =>
          throw s!"rule {label}: 'then' must be a string or have one of 'obligation'/'forbidden'/'counts_as'"

private def ruleFromJson (rd : Json) (i : Nat) : Except String Rule := do
  let label := (optStr rd "id").getD s!"r{i + 1}"
  let strength := (optStr rd "strength").getD "defeasible"
  if strength != "defeasible" && strength != "defeater" then
    throw s!"rule {label}: strength must be defeasible|defeater"
  let ifArr ← optArr rd "if"
  let body ← ifArr.mapM (fun x => do let s ← x.getStr?; parseBodyElem s)
  let thenJ ← (match rd.getObjVal? "then" with
    | .ok v => pure v
    | .error _ => throw s!"rule {label}: missing 'then'")
  let (mode, head) ← headFromJson thenJ (optStr rd "kind") label
  return { label := label, mode := mode, strength := strength, body := body, head := head,
           gloss := (optStr rd "gloss").getD "" }

def theoryFromJson (j : Json) : Except String Theory := do
  let factArr ← optArr j "facts"
  let facts ← factArr.mapM (fun x => do let s ← x.getStr?; parseLiteralStr s)
  let ruleArr ← optArr j "rules"
  let mut rules : List Rule := []
  let mut labels : List String := []
  let mut i := 0
  for rd in ruleArr do
    let rule ← ruleFromJson rd i
    if labels.contains rule.label then throw s!"duplicate rule id {rule.label}"
    labels := labels ++ [rule.label]
    rules := rules ++ [rule]
    i := i + 1
  let supArr ← optArr j "superiority"
  let mut sup : List (String × String) := []
  for pair in supArr do
    let arr ← pair.getArr?
    if arr.size != 2 then throw "superiority entry must be a pair"
    let weaker ← arr[0]!.getStr?
    let stronger ← arr[1]!.getStr?
    if !labels.contains weaker then throw s!"superiority references unknown rule {weaker}"
    if !labels.contains stronger then throw s!"superiority references unknown rule {stronger}"
    sup := sup ++ [(weaker, stronger)]
  return { facts := facts, rules := rules, superiority := sup }

def theoryFromJsonStr (s : String) : Except String Theory := do
  let j ← Json.parse s
  theoryFromJson j

-- ---------------------------------------------------------------- serialisation
private def elemToToken (b : BodyElem) : String :=
  match b with
  | .modal m => (if m.neg then "-" else "") ++ m.op ++ " " ++ toString m.lit
  | .plain l => toString l

def ruleToJson (r : Rule) : Json :=
  let base : List (String × Json) :=
    [("id", Json.str r.label), ("strength", Json.str r.strength),
     ("if", Json.arr ((r.body.map (fun b => Json.str (elemToToken b))).toArray))]
  let kindThen : List (String × Json) :=
    if r.mode == "C" then
      [("kind", Json.str "constitutive"),
       ("then", Json.mkObj [("counts_as", Json.str (toString (r.head.headD BOTTOM)))])]
    else
      [("kind", Json.str "prescriptive"),
       ("then", Json.mkObj [("obligation", Json.arr ((r.head.map (fun h => Json.str (toString h))).toArray))])]
  let gloss := if r.gloss != "" then [("gloss", Json.str r.gloss)] else []
  Json.mkObj (base ++ kindThen ++ gloss)

def theoryToJson (theory : Theory) : Json :=
  let facts := (theory.facts.map (fun f => Json.str (toString f))).toArray
  let rules := (theory.rules.map ruleToJson).toArray
  let sup := (theory.superiority.map (fun (w, s) => Json.arr #[Json.str w, Json.str s])).toArray
  Json.mkObj [("facts", Json.arr facts), ("rules", Json.arr rules), ("superiority", Json.arr sup)]

end Ddl
