import Deontic.Theory
import Deontic.ProofTags
import Deontic.Query

namespace Deontic.Pretty

-- ── Plain text rendering ──────────────────────────────────────────────────────

def renderTaggedLit (tl : TaggedLit) : String :=
  let sign := if tl.positive then "+∂" else "-∂"
  s!"{sign}_{tl.modality} {tl.lit}"

def renderUnresolvedConflict (c : UnresolvedConflict) : String :=
  let pairLines := c.pairs.map fun (r, s) =>
    s!"  {r}  and  {s}  conflict with no superiority (judge: add {r} > {s}  or  {s} > {r})"
  let header :=
    s!"[unresolved obligation conflict on {c.atom}]\n" ++
    s!"  neither O({c.atom}) nor O(~{c.atom}) is provable (+∂)\n" ++
    s!"  rules for O({c.atom}): {", ".intercalate c.forO}\n" ++
    s!"  rules for O(~{c.atom}): {", ".intercalate c.againstO}"
  header ++ "\n" ++ "\n".intercalate pairLines

def renderUnresolvedConflicts (ext : Extension) : String :=
  "\n\n".intercalate (ext.unresolvedConflicts.map renderUnresolvedConflict)

def renderExtension (ext : Extension) : String :=
  let lines := ext.derivation.toList.map renderTaggedLit
  let viol := if ext.hasViolation then ["[NON-COMPENSABLE VIOLATION]"] else []
  let judge := if ext.hasUnresolvedConflicts then [renderUnresolvedConflicts ext] else []
  (lines ++ viol ++ judge).foldl (· ++ "\n" ++ ·) ""

def renderQueryResults (atoms : List Atom) (ext : Extension) : String :=
  atoms.foldl (fun acc a =>
    let status := normativeStatus ext a
    let pad := if a.length < 20 then String.ofList (List.replicate (20 - a.length) ' ') else ""
    let padded := pad ++ a
    acc ++ s!"{padded} : {status}\n") ""

def renderQueryResultsWithTrace (atoms : List Atom) (ext : Extension) : String :=
  atoms.foldl (fun acc a =>
    let status := normativeStatus ext a
    let tags := ext.tagsFor a |>.map renderTaggedLit
    let trace := if tags.isEmpty then "  (no tags derived)"
                 else tags.foldl (fun s t => s ++ "\n  " ++ t) ""
    acc ++ s!"{a} : {status}{trace}\n\n") ""

-- ── JSON rendering ────────────────────────────────────────────────────────────

private def jsonStr (s : String) : String := s!"\"{ s }\""

private def jsonBool (b : Bool) : String := if b then "true" else "false"

private def renderTagJSON (tl : TaggedLit) : String :=
  s!"\{\"positive\":{jsonBool tl.positive},\"modality\":{jsonStr (toString tl.modality)},\"literal\":{jsonStr (toString tl.lit)}}"

def renderAtomJSON (a : Atom) (ext : Extension) : String :=
  let status := normativeStatus ext a
  let tags   := ext.tagsFor a |>.map renderTagJSON
  let tagsStr := "[" ++ ",".intercalate tags ++ "]"
  s!"{jsonStr a}:\{\"status\":{jsonStr status},\"tags\":{tagsStr}}"

private def renderConflictJSON (c : UnresolvedConflict) : String :=
  let pairs := c.pairs.map fun (r, s) => "[" ++ jsonStr r ++ "," ++ jsonStr s ++ "]"
  "{\"atom\":" ++ jsonStr c.atom ++
    ",\"forO\":[" ++ ", ".intercalate (c.forO.map jsonStr) ++
    "],\"againstO\":[" ++ ", ".intercalate (c.againstO.map jsonStr) ++
    "],\"unresolvedPairs\":[" ++ ", ".intercalate pairs ++ "]}"

def renderExtensionJSON (atoms : List Atom) (ext : Extension) : String :=
  let entries := atoms.map (renderAtomJSON · ext)
  let viol := s!"\"hasViolation\":{jsonBool ext.hasViolation}"
  let conflicts := ext.unresolvedConflicts.map renderConflictJSON
  let judge :=
    s!"\"hasUnresolvedConflicts\":{jsonBool ext.hasUnresolvedConflicts},\"unresolvedConflicts\":[{String.intercalate ", " conflicts}]"
  "{\n" ++ ",\n".intercalate (entries ++ [viol, judge]) ++ "\n}"

end Deontic.Pretty
