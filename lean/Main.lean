/-
Command-line interface mirroring the Python `ddl` CLI.

    ddl run    THEORY [--facts "a. -b."] [--all]   -- compute and report verdicts
    ddl query  THEORY QUERY [--facts ...] [--no-trace]
    ddl render THEORY                                -- theory back in English

THEORY is a `.ddl` file, or a `.json` file (or pass `--json`).
-/
import Ddl
open Ddl

structure Opts where
  positional : List String := []
  facts      : Option String := none
  all        : Bool := false
  noTrace    : Bool := false
  json       : Bool := false

def parseOpts : List String → Opts
  | [] => {}
  | "--facts" :: v :: rest => { parseOpts rest with facts := some v }
  | "--all" :: rest => { parseOpts rest with all := true }
  | "--no-trace" :: rest => { parseOpts rest with noTrace := true }
  | "--json" :: rest => { parseOpts rest with json := true }
  | a :: rest => let o := parseOpts rest; { o with positional := a :: o.positional }

def loadTheory (path : String) (asJson : Bool) : IO (Except String Theory) := do
  let text ← IO.FS.readFile path
  if asJson || path.endsWith ".json" then return theoryFromJsonStr text
  else return parse text

def addFacts (t : Theory) : Option String → Except String Theory
  | none => .ok t
  | some s => (parse s).map (fun ft => t.withFacts ft.facts)

def usage : String :=
  "usage: ddl (run|query|render) THEORY [QUERY] [--facts \"a. -b.\"] [--all] [--no-trace] [--json]"

def main (args : List String) : IO UInt32 := do
  match args with
  | [] => IO.eprintln usage; return 2
  | cmd :: rest =>
    let o := parseOpts rest
    match o.positional with
    | [] => IO.eprintln usage; return 2
    | path :: more =>
      match ← loadTheory path o.json with
      | .error e => IO.eprintln s!"error: {e}"; return 2
      | .ok t0 =>
        if cmd == "render" then
          IO.println (describeTheory t0); return 0
        match addFacts t0 o.facts with
        | .error e => IO.eprintln s!"error: {e}"; return 2
        | .ok t =>
          let r := Reasoner.ofTheory t
          if cmd == "run" then
            IO.println (r.report (concise := !o.all)); return 0
          else if cmd == "query" then
            match more with
            | q :: _ => IO.println (toString (r.queryStr q (trace := !o.noTrace))); return 0
            | [] => IO.eprintln "error: query requires a QUERY argument"; return 2
          else
            IO.eprintln usage; return 2
