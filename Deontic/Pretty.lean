import Deontic.Theory
import Deontic.ProofTags
import Deontic.Query
import Deontic.Abduce

namespace Deontic.Pretty

-- ── Plain text rendering ──────────────────────────────────────────────────────

private def bearerTag : Option String → String
  | some p => s!"@{p}"
  | none   => ""

def renderTaggedLit (tl : TaggedLit) : String :=
  let sign := if tl.positive then "+∂" else "-∂"
  s!"{sign}_{tl.modality}{bearerTag tl.bearer} {tl.lit}"

def renderUnresolvedConflict (c : UnresolvedConflict) : String :=
  let pairLines := c.pairs.map fun (r, s) =>
    s!"  {r}  and  {s}  conflict with no superiority (judge: add {r} > {s}  or  {s} > {r})"
  let who := match c.bearer with | some p => s!" (bearer {p})" | none => ""
  let header :=
    s!"[unresolved obligation conflict on {c.atom}{who}]\n" ++
    s!"  neither O{bearerTag c.bearer}({c.atom}) nor O{bearerTag c.bearer}(~{c.atom}) is provable (+∂)\n" ++
    s!"  rules for O({c.atom}): {", ".intercalate c.forO}\n" ++
    s!"  rules for O(~{c.atom}): {", ".intercalate c.againstO}"
  header ++ "\n" ++ "\n".intercalate pairLines

def renderUnresolvedConflicts (ext : Extension) : String :=
  "\n\n".intercalate (ext.unresolvedConflicts.map renderUnresolvedConflict)

-- ── Non-compensable violation report ─────────────────────────────────────────

/-- The arrow that produced this rule, e.g. `=>O` (prescriptive defeasible). -/
private def renderArrow (r : Rule) : String :=
  toString r.strength ++ (if r.family == .prescriptive then "O" else "")
    ++ (match r.bearer with | some p => s!"@{p}" | none => "")

/-- Formal one-line rendering of a rule: `label: body  =>O  c1 * c2 * …`. -/
def renderRule (r : Rule) : String :=
  let body := if r.antecedent.isEmpty then ""
              else ", ".intercalate (r.antecedent.map toString) ++ "  "
  s!"{r.label}: {body}{renderArrow r}  {r.conclusion.toStr}"

/-- A literal as plain English, using the atom's description. `~a` reads as the
negation of the description. Falls back to the bare name if undescribed. -/
private def litEnglish (thy : Theory) (l : Lit) : String :=
  let desc := (thy.atomDecl? l.atom).map (·.description) |>.getD "(no description)"
  match l with
  | .pos _ => desc
  | .neg _ => s!"NOT ({desc})"

/-- Why a chain literal counts as violated in the current facts. -/
private def violReason (ci : Lit) : String :=
  match ci with
  | .pos a => s!"required, but '{a}' is not among the facts"
  | .neg a => s!"prohibited, but '{a}' is among the facts"

/-- Human-legible explanation of the non-compensable violation: which rules fired
and why no remedy remains. Each violating rule's whole obligation chain is shown
with the English meaning of every atom, so a reader needs no other reference. -/
def renderViolationReport (thy : Theory) (ext : Extension) : String :=
  let rules := ext.violatingRuleLabels.filterMap (fun lbl => thy.rules.find? (·.label == lbl))
  let intro :=
    "Rules causing the rejection (every obligation in each chain is itself\n" ++
    "obligated and breached, so no compensation remains):"
  let block (r : Rule) : String :=
    let chain := r.conclusion.map fun ci =>
      s!"    - O({ci}) — \"{litEnglish thy ci}\"\n        {violReason ci}"
    s!"  • {renderRule r}\n" ++ "\n".intercalate chain
  intro ++ "\n\n" ++ "\n\n".intercalate (rules.map block)

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
  let bearer := match tl.bearer with | some p => jsonStr p | none => "null"
  s!"\{\"positive\":{jsonBool tl.positive},\"modality\":{jsonStr (toString tl.modality)},\"bearer\":{bearer},\"literal\":{jsonStr (toString tl.lit)}}"

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
  let viol :=
    s!"\"hasViolation\":{jsonBool ext.hasViolation}," ++
    s!"\"violatingRules\":[{", ".intercalate (ext.violatingRuleLabels.map jsonStr)}]"
  let conflicts := ext.unresolvedConflicts.map renderConflictJSON
  let judge :=
    s!"\"hasUnresolvedConflicts\":{jsonBool ext.hasUnresolvedConflicts},\"unresolvedConflicts\":[{String.intercalate ", " conflicts}]"
  "{\n" ++ ",\n".intercalate (entries ++ [viol, judge]) ++ "\n}"

-- ── Abduction rendering ───────────────────────────────────────────────────────

def renderConfig (c : Config) : String :=
  if c.isEmpty then "{ }  (no facts needed)"
  else "{ " ++ ", ".intercalate (c.map toString) ++ " }"

def renderConditions (cs : List Condition) : String :=
  ", ".intercalate (cs.map toString)

/-- Human-readable abduction report.  When `showAll` is false only the first
`limit` minimal configurations are listed. -/
def renderAbduceResult (res : AbduceResult) (showAll : Bool) (limit : Nat) : String :=
  let header := s!"Goal: {renderConditions res.conds}"
  let forcedLine :=
    if res.forced.isEmpty then ""
    else s!"\nAssuming facts: {", ".intercalate (res.forced.map toString)}"
  if res.minimal.isEmpty then
    let warn :=
      if res.truncated then
        s!"\n(search truncated at {res.cap} configurations; result may be incomplete — pin atoms with --assume)"
      else ""
    header ++ forcedLine ++
      "\nNo fact configuration over the abducible atoms makes the goal hold." ++ warn
  else
    let total := res.minimal.length
    let shown := if showAll then res.minimal else res.minimal.take limit
    let lines := shown.zipIdx.map fun (c, i) => s!"  {i + 1}. {renderConfig c}"
    let countLine :=
      s!"\n{total} minimal configuration(s) make the goal hold ({res.satisfying} satisfying of {res.evaluated} evaluated):"
    let more :=
      if !showAll && total > limit then
        s!"\n  … {total - limit} more (use --all to list every minimal configuration)"
      else ""
    let warn :=
      if res.truncated then
        s!"\n(search truncated at {res.cap} configurations; pin atoms with --assume for completeness)"
      else ""
    header ++ forcedLine ++ countLine ++ "\n" ++ "\n".intercalate lines ++ more ++ warn

-- ── Atom descriptions / provenance ────────────────────────────────────────────

/-- One atom's grounding. `resolved` is the text fetched from the provenance
URI (when `--resolve` found a local markdown file); otherwise omitted. -/
def renderAtomEntry (a : Atom) (decl : Option AtomDecl) (resolved : Option String) : String :=
  match decl with
  | none => s!"{a}\n  (no description — undefined)"
  | some d =>
    let provLines := match d.provenance with
      | none   => ""
      | some p =>
        let q := match p.quote with | some x => s!"\n  quote: {x}" | none => ""
        let u := match p.uri   with | some x => s!"\n  uri:   {x}" | none => ""
        q ++ u
    let resLine := match resolved with
      | none   => ""
      | some t => s!"\n  text:  {t.trimAscii.toString}"
    s!"{a}\n  desc:  {d.description}{provLines}{resLine}"

/-- Render the whole atom dictionary (one entry per Herbrand-base atom). The
`resolve` map supplies fetched provenance text keyed by atom, when available. -/
def renderAtoms (thy : Theory) (resolved : Atom → Option String) : String :=
  "\n".intercalate (thy.herbrandBase.map fun a =>
    renderAtomEntry a (thy.atomDecl? a) (resolved a))

private def jsonOptStr : Option String → String
  | some x => jsonStr x
  | none   => "null"

def renderAtomsJSON (thy : Theory) (resolved : Atom → Option String) : String :=
  let entry (a : Atom) : String :=
    let d := thy.atomDecl? a
    let desc := match d with | some x => jsonStr x.description | none => "null"
    let prov := match d.bind (·.provenance) with
      | some p => s!"\{\"quote\":{jsonOptStr p.quote},\"uri\":{jsonOptStr p.uri}}"
      | none   => "null"
    let res  := jsonOptStr (resolved a)
    s!"\{\"atom\":{jsonStr a},\"description\":{desc},\"provenance\":{prov},\"resolved\":{res}}"
  "[" ++ ",\n".intercalate (thy.herbrandBase.map entry) ++ "]"

def renderAbduceResultJSON (res : AbduceResult) : String :=
  let litJSON (l : Lit) := jsonStr (toString l)
  let cfgJSON (c : Config) := "[" ++ ", ".intercalate (c.map litJSON) ++ "]"
  let conds := res.conds.map (fun c => jsonStr (toString c))
  let mins  := res.minimal.map cfgJSON
  "{\n" ++
    "\"goal\":[" ++ ", ".intercalate conds ++ "],\n" ++
    "\"assumedFacts\":[" ++ ", ".intercalate (res.forced.map litJSON) ++ "],\n" ++
    "\"minimalConfigs\":[" ++ ", ".intercalate mins ++ "],\n" ++
    s!"\"minimalCount\":{res.minimal.length},\n" ++
    s!"\"satisfying\":{res.satisfying},\n" ++
    s!"\"evaluated\":{res.evaluated},\n" ++
    s!"\"truncated\":{jsonBool res.truncated}\n}"

end Deontic.Pretty
