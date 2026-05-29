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

-- ── Atom declaration parser ───────────────────────────────────────────────────
-- Syntax (one line):  atom NAME: description | <prov-seg> | <prov-seg> ...
-- Each provenance segment is `uri: <path>`, `quote: <text>`, or bare text
-- (treated as a quote). A `uri` must point to a markdown file and may carry a
-- GitHub-style line selector (`docs/sources/nda.md#L3-L5`). The whole line is
-- taken verbatim — no `#` comment stripping — so selectors survive; do not put
-- trailing `#` comments on atom lines.

private def trimS (s : String) : String := s.trimAscii.toString

private def uriPath (uri : String) : String :=
  (uri.splitOn "#").headD uri

private def addProvSeg (name : String) (p : Provenance) (seg : String) : Except String Provenance :=
  let s := trimS seg
  if s.isEmpty then .ok p
  else if s.startsWith "uri:" then
    let u := trimS (s.drop 4).toString
    if !(uriPath u |>.endsWith ".md") then
      .error s!"atom '{name}': provenance uri must point to a markdown (.md) file, got '{u}'"
    else .ok { p with uri := some u }
  else if s.startsWith "quote:" then
    .ok { p with quote := some (trimS (s.drop 6).toString) }
  else
    .ok { p with quote := some s }   -- bare text shorthand for a quote

-- ── Import declaration parser ──────────────────────────────────────────────────
-- `import <path> [as <alias>]`  or  `from <path> import *`
-- The path stem (filename without `.ddl`) is the default alias.

private def pathStem (path : String) : String :=
  let base := (path.splitOn "/").getLast!
  (base.splitOn ".").head!

private def parseImport (raw : String) : Except String ImportDecl :=
  let toks := (raw.splitOn " ").map trimS |>.filter (!·.isEmpty)
  match toks with
  | ["import", path]              => .ok (.namespaced path (pathStem path))
  | ["import", path, "as", alias] => .ok (.namespaced path alias)
  | ["from", path, "import", "*"] => .ok (.glob path)
  | "from" :: _ =>
    .error "only `from <path> import *` is supported (selective import not yet implemented)"
  | _ => .error s!"malformed import: '{raw}'"

private def parseAtomDecl (raw : String) : Except String AtomDecl := do
  let afterKw := (raw.drop 5).toString          -- drop "atom "
  match afterKw.splitOn ":" with
  | [] => .error "malformed atom declaration"
  | name :: rest =>
    let name := trimS name
    if name.isEmpty then .error "atom declaration with empty name"
    let body := trimS (":".intercalate rest)
    let segs := body.splitOn "|"
    let desc := trimS segs.head!
    if desc.isEmpty then .error s!"atom '{name}' has no description"
    let provSegs := segs.drop 1
    if provSegs.isEmpty then .ok ⟨name, desc, none⟩
    else
      let prov ← provSegs.foldlM (addProvSeg name) ({} : Provenance)
      if prov.isEmpty then
        .error s!"atom '{name}' has an empty provenance ('|' with nothing usable after)"
      else .ok ⟨name, desc, some prov⟩

-- ── Main entry point ─────────────────────────────────────────────────────────

def parse (src : String) : Except String Theory := do
  let lines := src.splitOn "\n"
  let mut facts       : List Lit       := []
  let mut rules       : List Rule      := []
  let mut superiority : SuperiorityRel := []
  let mut atoms       : List AtomDecl  := []
  let mut imports     : List ImportDecl := []

  for rawLine in lines do
    let rawTrim := rawLine.trimAscii.toString
    -- Atom declarations are read verbatim (no `#` comment stripping) so that
    -- provenance URIs may contain `#` fragments.
    if rawTrim.startsWith "atom " then
      let decl ← parseAtomDecl rawTrim
      atoms := atoms ++ [decl]
      continue
    if rawTrim.startsWith "import " || rawTrim.startsWith "from " then
      let imp ← parseImport ((rawTrim.splitOn "#").head!.trimAscii.toString)
      imports := imports ++ [imp]
      continue

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

  .ok ⟨facts, rules, superiority, atoms, imports⟩

end Deontic.Parser
