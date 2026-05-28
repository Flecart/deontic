import Deontic.Theory
import Deontic.Extension
import Deontic.Query
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
  IO.println "Arrow syntax in .ddl files:"
  IO.println "  ->   strict constitutive    ->O  strict prescriptive"
  IO.println "  =>   defeasible constitutive  =>O  defeasible prescriptive"
  IO.println "  ~>   defeater constitutive    ~>O  defeater prescriptive"
  IO.println "  >    superiority: r1 > r2 means r1 defeats r2"
  IO.println "  ~p   negation of atom p"
  IO.println "  *    compensatory chain: a * b * c"

def loadTheory (file : String) : IO Theory := do
  let src ← IO.FS.readFile file
  match parse src with
  | .error e =>
    IO.eprintln s!"Parse error: {e}"
    IO.Process.exit 1
  | .ok thy => return thy

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
  | _ =>
    IO.eprintln s!"Unknown command '{cmd}'. Use 'check' or 'query'."
    IO.Process.exit 1
