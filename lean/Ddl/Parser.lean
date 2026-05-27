/-
Parser for the `.ddl` surface syntax (human / test authoring).

Grammar (statement-oriented; statements separated by newlines or `.`):

    fact         := literal
    rule         := [label ":"] body arrow head
    superiority  := label "<" label          -- left < right  ==>  right is superior
    comment      := "#" ... end-of-line

    arrow        := ("=>" | "~>") [mode]      -- => defeasible, ~> defeater
    mode         := "C" | "O"                 -- attached to arrow; default C
    body         := [ elem ("," elem)* ]
    head         := literal ("(x)" literal)*  -- otimes chain; singleton for C
    elem         := modal | literal
    modal        := ["-"] ("O"|"F"|"P"|"Pw"|"Ps") WS literal
    literal      := ["-"] atom
    atom         := [A-Za-z_][A-Za-z0-9_]*

`F x` is parsed to `O(~x)` (eq. 3). `r < s` records `(r, s)` meaning s is
superior to r. A direct port of `src/ddl/parser.py`.
-/
import Ddl.Syntax

namespace Ddl

def bottomNames : List String := ["bottom", "⊥", "_bottom", "_|_"]
def modalOps : List String := ["O", "F", "Pw", "Ps", "P"]

def isAtomStart (c : Char) : Bool := c.isAlpha || c == '_'
def isAtomChar (c : Char) : Bool := c.isAlpha || c.isDigit || c == '_'

/-- Lean 4.30's `String.trim`/`take`/`drop` return `String.Slice`; we keep
`String`-valued versions to avoid threading slices everywhere. -/
def trim (s : String) : String :=
  let cs := s.toList.dropWhile Char.isWhitespace
  String.ofList (cs.reverse.dropWhile Char.isWhitespace).reverse

def stake (s : String) (n : Nat) : String := String.ofList (s.toList.take n)
def sdrop (s : String) (n : Nat) : String := String.ofList (s.toList.drop n)
def sfront (s : String) : Char := s.toList.headD ' '

def isValidAtom (s : String) : Bool :=
  match s.toList with
  | [] => false
  | c :: cs => isAtomStart c && cs.all isAtomChar

partial def listIndexOfAux (needle : List Char) (i : Nat) (rest : List Char) : Option Nat :=
  if needle.isPrefixOf rest then some i
  else match rest with
    | [] => none
    | _ :: t => listIndexOfAux needle (i + 1) t

/-- First char-index of `sub` in `s`, if present. -/
def strIndexOf (s sub : String) : Option Nat := listIndexOfAux sub.toList 0 s.toList

def strContains (s sub : String) : Bool := (strIndexOf s sub).isSome

def parseLiteralStr (text : String) : Except String Literal :=
  let t := trim text
  if bottomNames.contains t then .ok BOTTOM
  else
    let (neg, rest) := if t.startsWith "-" then (true, sdrop t 1) else (false, t)
    if isValidAtom rest then .ok { atom := rest, neg := neg }
    else .error s!"invalid literal: {text}"

def tryModal (text : String) : Option ModalLiteral :=
  let t := trim text
  let (outerNeg, rest1) := if t.startsWith "-" then (true, sdrop t 1) else (false, t)
  let tryOp (op : String) : Option ModalLiteral :=
    if rest1.startsWith op then
      let after := sdrop rest1 op.length
      if after.length > 0 && (sfront after).isWhitespace then
        match (parseLiteralStr (trim after)).toOption with
        | some inner =>
          if op == "F" then some { op := "O", lit := inner.complement, neg := outerNeg }
          else some { op := op, lit := inner, neg := outerNeg }
        | none => none
      else none
    else none
  modalOps.findSome? tryOp

def parseBodyElem (text : String) : Except String BodyElem :=
  match tryModal text with
  | some m => .ok (.modal m)
  | none => (parseLiteralStr text).map .plain

/-- Return (body_str, strength, mode, head_str). -/
def splitArrow (text : String) : Except String (String × String × String × String) :=
  if strContains text "->" then .error "strict rules ('->') are not supported"
  else
    let splitFirst (tok : String) : String × String :=
      match text.splitOn tok with
      | b :: rest@(_ :: _) => (b, String.intercalate tok rest)
      | _ => (text, "")
    let arrow? : Option (String × String) :=
      if strContains text "=>" then some ("=>", "defeasible")
      else if strContains text "~>" then some ("~>", "defeater")
      else none
    match arrow? with
    | none => .error s!"no rule arrow in: {text}"
    | some (token, strength) =>
      let (bodyStr, after0) := splitFirst token
      let rest1 := sdrop after0 1
      let (mode, after) :=
        if after0.length ≥ 1 && (sfront after0 == 'C' || sfront after0 == 'O')
            && (after0.length == 1 || (sfront rest1).isWhitespace) then
          (String.singleton (sfront after0), rest1)
        else ("C", after0)
      .ok (bodyStr, strength, mode, after)

def parseHead (text : String) : Except String (List Literal) := do
  let parts := text.splitOn "(x)"
  let lits ← parts.mapM parseLiteralStr
  return normalizeChain lits

def parseRule (stmt : String) (autoLabel : String) : Except String Rule := do
  let arrowPos? : Option Nat :=
    match strIndexOf stmt "=>", strIndexOf stmt "~>" with
    | some a, some b => some (min a b)
    | some a, none => some a
    | none, some b => some b
    | none, none => none
  let colon? := strIndexOf stmt ":"
  let (label, headSide) :=
    match colon? with
    | some c =>
      let beforeArrow := match arrowPos? with | none => true | some a => c < a
      if beforeArrow then (trim (stake stmt c), sdrop stmt (c + 1)) else (autoLabel, stmt)
    | none => (autoLabel, stmt)
  let (bodyStr, strength, mode, headStr) ← splitArrow headSide
  let bodyParts := (bodyStr.splitOn ",").filter (fun b => trim b != "")
  let body ← bodyParts.mapM parseBodyElem
  let head ← parseHead headStr
  if head.isEmpty || trim headStr == "" then
    .error s!"rule {label} has empty head"
  else
    .ok { label := label, mode := mode, strength := strength, body := body, head := head }

def splitOnChars (s : String) (seps : List Char) : List String :=
  let step := s.foldl (fun (acc : List String × String) c =>
      if seps.contains c then (acc.1 ++ [acc.2], "") else (acc.1, acc.2.push c))
    ([], "")
  step.1 ++ [step.2]

def statements (source : String) : List String :=
  let stripped := (source.splitOn "\n").map (fun line => (line.splitOn "#").headD "")
  let cleaned := String.intercalate "\n" stripped
  (splitOnChars cleaned ['.', '\n']).map trim |>.filter (· != "")

def validate (theory : Theory) : Except String Unit := do
  let labels := theory.rules.map (·.label)
  for (weaker, stronger) in theory.superiority do
    if !labels.contains weaker then throw s!"superiority references unknown rule {weaker}"
    if !labels.contains stronger then throw s!"superiority references unknown rule {stronger}"
  return ()

def parse (source : String) : Except String Theory := do
  let mut theory : Theory := {}
  let mut auto := 0
  for stmt in statements source do
    if strContains stmt "=>" || strContains stmt "~>" then
      auto := auto + 1
      let rule ← parseRule stmt s!"_r{auto}"
      theory := { theory with rules := theory.rules ++ [rule] }
    else if strContains stmt "<" then
      match stmt.splitOn "<" with
      | left :: rest@(_ :: _) =>
        theory := { theory with superiority :=
          theory.superiority ++ [(trim left, trim (String.intercalate "<" rest))] }
      | _ => pure ()
    else
      let l ← parseLiteralStr stmt
      theory := { theory with facts := theory.facts ++ [l] }
  validate theory
  return theory

/-- Parse, panicking on error. For tests / `#eval`. -/
def parse! (source : String) : Theory :=
  match parse source with
  | .ok t => t
  | .error e => panic! s!"parse error: {e}"

def parseFile (path : System.FilePath) : IO (Except String Theory) := do
  let text ← IO.FS.readFile path
  return parse text

end Ddl
