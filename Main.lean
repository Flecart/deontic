import Deontic.Theory
import Deontic.Extension
import Deontic.Query
import Deontic.Abduce
import Deontic.Parser
import Deontic.Pretty

open Deontic Deontic.Parser Deontic.Pretty

def printHelp : IO Unit := do
  IO.println "Defeasible Deontic Logic reasoner"
  IO.println ""
  IO.println "Usage:"
  IO.println "  deontic check <file.ddl> [--json]"
  IO.println "    Compute the full extension of the theory."
  IO.println ""
  IO.println "  deontic query <file.ddl> <atom> [...] [--json] [--trace]"
  IO.println "    Query normative status of specific atoms."
  IO.println ""
  IO.println "  deontic atoms <file.ddl> [--json] [--resolve]"
  IO.println "    Print every atom with its description and provenance"
  IO.println "    (for an LLM/human to know what each atom means)."
  IO.println "    --resolve inlines provenance that points to a local file."
  IO.println ""
  IO.println "  deontic abduce <file.ddl> <goal> [more-conditions...]"
  IO.println "                 [--all] [--limit N] [--assume t,...] [--json]"
  IO.println "    Find fact configurations that make the goal hold."
  IO.println "    Goal/condition tokens (prefix ! = must NOT hold):"
  IO.println "      O(a) F(a) P(a) Ps(a) Pw(a) C(a)   a   ~a"
  IO.println "    e.g.  P(Disclose)            configurations that ALLOW Disclose"
  IO.println "          O(use)                 configurations that REQUIRE use"
  IO.println "          P(Disclose) !C(Notify)  Disclose allowed while Notify absent"
  IO.println "    --assume tokens pin facts and shrink the search:"
  IO.println "      a (true)   ~a (false)   -a (must stay absent)"
  IO.println ""
  IO.println "Arrow syntax in .ddl files:"
  IO.println "  ->   strict constitutive    ->O  strict prescriptive"
  IO.println "  =>   defeasible constitutive  =>O  defeasible prescriptive"
  IO.println "  ~>   defeater constitutive    ~>O  defeater prescriptive"
  IO.println "  >    superiority: r1 > r2 means r1 defeats r2"
  IO.println ""
  IO.println "When applicable rules conflict on O(a) vs O(~a) with no > between them,"
  IO.println "neither obligation is derived; the reasoner flags [JUDGE: ...] for the user."
  IO.println "  ~p   negation of atom p"
  IO.println "  *    compensatory chain: a * b * c"

private def parseFile (file : String) : IO Theory := do
  let src ← IO.FS.readFile file
  match parse src with
  | .error e =>
    IO.eprintln s!"Parse error in {file}: {e}"
    IO.Process.exit 1
  | .ok thy => return thy

/-- Directory of `file` (everything up to the last `/`), or "." if none. -/
private def dirOf (file : String) : String :=
  match (file.splitOn "/").dropLast with
  | [] => "."
  | parts => "/".intercalate parts

/-- Parse a theory and recursively resolve its `import` / `from … import *`
directives, namespacing or guard-merging each. Paths are relative to the
importing file. Does NOT enforce that atoms are described. -/
partial def resolveImports (visited : List String) (file : String) : IO Theory := do
  if visited.contains file then
    IO.eprintln s!"Error: import cycle through {file}"
    IO.Process.exit 1
  let thy ← parseFile file
  let dir := dirOf file
  let mut acc : Theory := { thy with imports := [] }
  for imp in thy.imports do
    let path := if (imp.path).startsWith "/" then imp.path else s!"{dir}/{imp.path}"
    let sub  ← resolveImports (file :: visited) path
    let nsSub := match imp with
      | .namespaced _ alias => sub.namespaced alias
      | .glob _             => sub
    match acc.mergeGuarded nsSub with
    | .ok merged => acc := merged
    | .error e   => IO.eprintln s!"Import error ({path}): {e}"; IO.Process.exit 1
  return acc

/-- Resolve imports; the `atoms` command must run on any file. -/
def loadTheoryRaw (file : String) : IO Theory :=
  resolveImports [] file

/-- Load a theory (with imports resolved) and require every used atom to carry
a description. -/
def loadTheory (file : String) : IO Theory := do
  let thy ← resolveImports [] file
  let missing := thy.undescribedAtoms
  unless missing.isEmpty do
    IO.eprintln s!"Error: atoms used without a description: {", ".intercalate missing}"
    IO.eprintln "  add `atom <name>: <description>` lines (descriptions are mandatory)"
    IO.Process.exit 1
  return thy

private def stripL (x : String) : String :=
  if x.startsWith "L" then (x.drop 1).toString else x

/-- Parse a GitHub-style line selector like `L3-L5` or `L3` into a 1-based range. -/
def parseLineRange (sel : String) : Option (Nat × Nat) :=
  match sel.splitOn "-" with
  | [a]    => (stripL a).toNat?.map fun n => (n, n)
  | [a, b] => match (stripL a).toNat?, (stripL b).toNat? with
    | some x, some y => some (x, y)
    | _, _ => none
  | _ => none

/-- Resolve an atom's provenance URI to inlined source text when it points to a
local markdown file (relative to the project). A `#Lx-Ly` selector slices lines.
Remote (`http(s)://`) URIs are left unresolved. -/
def resolveProvenance (p : Provenance) : IO (Option String) := do
  match p.uri with
  | none => return none
  | some uri =>
    if uri.startsWith "http://" || uri.startsWith "https://" then return none
    let parts := uri.splitOn "#"
    let rawPath := parts.headD uri
    let path := if rawPath.startsWith "file://" then (rawPath.drop 7).toString else rawPath
    let sel  := if parts.length > 1 then some ("#".intercalate (parts.drop 1)) else none
    try
      if ← System.FilePath.pathExists path then
        let content ← IO.FS.readFile path
        match sel.bind parseLineRange with
        | some (a, b) =>
          let lines := content.splitOn "\n"
          let chosen := (lines.drop (a - 1)).take (b + 1 - a)
          return some ("\n".intercalate chosen)
        | none => return some content
      else return none
    catch _ => return none

structure AbduceArgs where
  goals   : List String := []
  assumes : List String := []
  all     : Bool := false
  json    : Bool := false
  limit   : Nat := 8

partial def parseAbduceArgs (args : List String) (acc : AbduceArgs) : AbduceArgs :=
  match args with
  | [] => { acc with goals := acc.goals.reverse }
  | "--all"  :: rest => parseAbduceArgs rest { acc with all := true }
  | "--json" :: rest => parseAbduceArgs rest { acc with json := true }
  | "--limit" :: n :: rest =>
    parseAbduceArgs rest { acc with limit := (n.toNat?).getD acc.limit }
  | "--assume" :: v :: rest =>
    let toks := (v.splitOn ",").map (·.trimAscii.toString) |>.filter (!·.isEmpty)
    parseAbduceArgs rest { acc with assumes := acc.assumes ++ toks }
  | tok :: rest => parseAbduceArgs rest { acc with goals := tok :: acc.goals }

def main (args : List String) : IO Unit := do
  if args.isEmpty || args.head! == "--help" || args.head! == "-h" then
    printHelp
    return

  let cmd  := args.head!
  let rest := args.tail

  match cmd with
  | "check" | "query" =>
    if rest.isEmpty then
      IO.eprintln "Error: missing .ddl file argument"
      IO.Process.exit 1
    let file   := rest.head!
    let flags  := rest.tail
    let thy    ← loadTheory file
    let useJSON  := flags.contains "--json"
    let useTrace := flags.contains "--trace"
    -- atom arguments: everything that isn't a flag
    let atomArgs := flags.filter (fun s => !s.startsWith "--")

    let ext := computeExtension thy

    if cmd == "check" then
      if useJSON then
        IO.println (renderExtensionJSON thy.herbrandBase ext)
      else do
        IO.println (renderExtension ext)
        if ext.hasViolation then
          IO.println "WARNING: non-compensable violation detected"
        if ext.hasUnresolvedConflicts then
          IO.println ""
          IO.println (renderUnresolvedConflicts ext)
          IO.println "WARNING: unresolved obligation conflict — judge must add superiority"
    else  -- query
      let targets :=
        if atomArgs.isEmpty then thy.herbrandBase
        else atomArgs
      if useJSON then
        IO.println (renderExtensionJSON targets ext)
      else if useTrace then
        IO.println (renderQueryResultsWithTrace targets ext)
      else
        IO.println (renderQueryResults targets ext)
      if ext.hasViolation then
        IO.println "WARNING: non-compensable violation detected"
      if ext.hasUnresolvedConflicts then
        IO.println ""
        IO.println (renderUnresolvedConflicts ext)
        IO.println "WARNING: unresolved obligation conflict — judge must add superiority"
  | "abduce" =>
    if rest.isEmpty then
      IO.eprintln "Error: missing .ddl file argument"
      IO.Process.exit 1
    let file := rest.head!
    let thy  ← loadTheory file
    let a    := parseAbduceArgs rest.tail {}
    if a.goals.isEmpty then
      IO.eprintln "Error: abduce needs at least one goal, e.g. 'P(Disclose)'"
      IO.Process.exit 1
    let conds ← match a.goals.mapM parseCondition with
      | .error e => IO.eprintln s!"Goal error: {e}"; IO.Process.exit 1
      | .ok cs   => pure cs
    let assumptions ← match a.assumes.mapM parseAssumption with
      | .error e => IO.eprintln s!"Assumption error: {e}"; IO.Process.exit 1
      | .ok xs   => pure xs
    let res := abduce thy assumptions conds
    if a.json then
      IO.println (renderAbduceResultJSON res)
    else
      IO.println (renderAbduceResult res a.all a.limit)
  | "atoms" =>
    if rest.isEmpty then
      IO.eprintln "Error: missing .ddl file argument"
      IO.Process.exit 1
    let file    := rest.head!
    let flags   := rest.tail
    let thy     ← loadTheoryRaw file   -- atoms must run even on undescribed files
    let useJSON := flags.contains "--json"
    let resolve := flags.contains "--resolve"
    -- Build a resolved-text lookup (only when --resolve and provenance is local).
    let mut resolvedPairs : List (Atom × String) := []
    if resolve then
      for a in thy.herbrandBase do
        match (thy.atomDecl? a).bind (·.provenance) with
        | none   => pure ()
        | some p => match ← resolveProvenance p with
          | none   => pure ()
          | some t => resolvedPairs := resolvedPairs ++ [(a, t)]
    let resolved : Atom → Option String := fun a =>
      (resolvedPairs.find? (·.1 == a)).map (·.2)
    if useJSON then
      IO.println (renderAtomsJSON thy resolved)
    else
      IO.println (renderAtoms thy resolved)
  | _ =>
    IO.eprintln s!"Unknown command '{cmd}'. Use 'check', 'query', 'abduce', or 'atoms'."
    IO.Process.exit 1
