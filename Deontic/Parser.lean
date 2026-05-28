import Deontic.Theory

namespace Deontic.Parser

-- ── Tokeniser ─────────────────────────────────────────────────────────────────

private def isDelim (c : Char) : Bool :=
  c == ',' || c == '(' || c == ')'

partial def tokenise (s : String) : List String :=
  let chars := s.toList
  let rec go (acc : List String) (cur : List Char) : List Char → List String
    | [] =>
      if cur.isEmpty then acc else acc ++ [String.ofList cur]
    | '#' :: rest =>
      let acc := if cur.isEmpty then acc else acc ++ [String.ofList cur]
      go acc [] (rest.dropWhile (· != '\n'))
    | c :: rest =>
      if c.isWhitespace || isDelim c then
        let acc := if cur.isEmpty then acc else acc ++ [String.ofList cur]
        let acc := if isDelim c then acc ++ [String.ofList [c]] else acc
        go acc [] rest
      else
        go acc (cur ++ [c]) rest
  go [] [] chars

-- ── Literal parsers ───────────────────────────────────────────────────────────

private def parseLit (s : String) : Except String Lit :=
  if s.startsWith "~" then
    let a := (s.drop 1).toString
    if a.isEmpty then .error "empty atom after ~"
    else .ok (.neg a)
  else if s.isEmpty then .error "empty literal"
  else .ok (.pos s)

private def deonticOpFromStr (s : String) : Option DeonticOp :=
  match s with
  | "Pw" => some .Pw
  | "Ps" => some .Ps
  | "O"  => some .O
  | "F"  => some .F
  | "P"  => some .P
  | _    => none

-- Parse a single token that may be a deontic literal like "O(foo)" or just "foo"
private def parseLiteral (tok : String) : Except String Literal := do
  -- Check if it starts with a known deontic op followed by "("
  let opPrefixes := ["Pw(", "Ps(", "O(", "F(", "P("]
  match opPrefixes.find? (tok.startsWith ·) with
  | some pfx =>
    let opStr := (pfx.dropEnd 1).toString   -- e.g. "O(" → "O"
    let inner := (tok.drop pfx.length).dropEnd 1 |>.toString
    let op ← (deonticOpFromStr opStr).elim (.error s!"unknown op {opStr}") .ok
    let lit ← parseLit inner
    .ok (.deontic ⟨op, lit⟩)
  | none =>
    let lit ← parseLit tok
    .ok (.plain lit)

-- ── Rule arrow parser ─────────────────────────────────────────────────────────

private def parseArrow (s : String) : Except String (RuleStrength × RuleFamily) :=
  match s with
  | "->"  => .ok (.strict,     .constitutive)
  | "->O" => .ok (.strict,     .prescriptive)
  | "=>"  => .ok (.defeasible, .constitutive)
  | "=>O" => .ok (.defeasible, .prescriptive)
  | "~>"  => .ok (.defeater,   .constitutive)
  | "~>O" => .ok (.defeater,   .prescriptive)
  | _     => .error s!"unknown arrow '{s}'"

-- ── OExpr parser ──────────────────────────────────────────────────────────────

private def parseOExpr (tokens : List String) : Except String OExpr :=
  let toks := tokens.filter (· != "*")
  if toks.isEmpty then .error "empty conclusion"
  else toks.mapM parseLit

-- ── Antecedent parser ─────────────────────────────────────────────────────────
-- Re-join split deontic tokens: ["O", "(", "foo", ")"] → ["O(foo)"]

private def joinDeonticTokens (tokens : List String) : List String :=
  let deonticOps := ["Pw", "Ps", "O", "F", "P"]
  let rec go (acc : List String) : List String → List String
    | tok :: "(" :: inner :: ")" :: rest =>
      if deonticOps.contains tok then
        go ((tok ++ "(" ++ inner ++ ")") :: acc) rest
      else
        go (")" :: inner :: "(" :: tok :: acc) rest
    | tok :: rest => go (tok :: acc) rest
    | [] => acc.reverse
  go [] tokens

private def parseAntecedent (tokens : List String) : Except String (List Literal) :=
  -- Commas only separate antecedent conjuncts; drop them so "a, b, c" does not
  -- parse the separators as spurious atoms (which would never be facts and so
  -- would make every multi-condition rule un-applicable).
  joinDeonticTokens (tokens.filter (· != ",")) |>.mapM parseLiteral

-- ── Rule line parser ──────────────────────────────────────────────────────────

private def isArrow (s : String) : Bool :=
  s == "->" || s == "->O" || s == "=>" || s == "=>O" || s == "~>" || s == "~>O"

private def parseRule (label : String) (tokens : List String) : Except String Rule := do
  match tokens.findIdx? isArrow with
  | none => .error s!"no arrow in rule '{label}'"
  | some arrowIdx =>
    let antToks  := tokens.take arrowIdx
    let arrowTok := tokens[arrowIdx]!
    let conToks  := tokens.drop (arrowIdx + 1)
    let (strength, family) ← parseArrow arrowTok
    let ant ← parseAntecedent antToks
    let con ← parseOExpr conToks
    .ok ⟨label, strength, family, ant, con⟩

-- ── Superiority line parser ───────────────────────────────────────────────────

private def parseSup (tokens : List String) : Except String SuperiorityRel :=
  let rec go (acc : SuperiorityRel) : List String → Except String SuperiorityRel
    | [] => .ok acc.reverse
    | l :: ">" :: r :: rest => go ((l, r) :: acc) rest
    | _ :: rest => go acc rest
  go [] tokens

-- ── Facts parser ─────────────────────────────────────────────────────────────

private def parseFacts (tokens : List String) : Except String (List Lit) :=
  tokens.filter (· != ",") |>.mapM parseLit

-- ── Main entry point ─────────────────────────────────────────────────────────

def parse (src : String) : Except String Theory := do
  let lines := src.splitOn "\n"
  let mut facts       : List Lit       := []
  let mut rules       : List Rule      := []
  let mut superiority : SuperiorityRel := []

  for rawLine in lines do
    let line := ((rawLine.splitOn "#").head!.trimAscii).toString
    if line.isEmpty then continue

    let parts := line.splitOn ":"
    if parts.length < 2 then continue
    let key  := parts[0]!.trimAscii.toString
    let rest := (parts.drop 1 |> ":".intercalate).trimAscii.toString
    let tokens := tokenise rest

    match key with
    | "facts" =>
      let fs ← parseFacts tokens
      facts := facts ++ fs
    | "superiority" =>
      let sups ← parseSup tokens
      superiority := superiority ++ sups
    | label =>
      if label.isEmpty then continue
      let rule ← parseRule label tokens
      rules := rules ++ [rule]

  .ok ⟨facts, rules, superiority⟩

end Deontic.Parser
