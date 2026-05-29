import Deontic.Theory
import Deontic.Extension
import Deontic.Query
import Deontic.Abduce
import Deontic.Parser
import Deontic.Pretty

open Deontic Deontic.Pretty

-- ── Example 1: License contract (§4) ─────────────────────────────────────────
-- Scenario A: license + publish + remove (illegal publish, then remedied)

def ex1Theory : Theory where
  facts := [.pos "license", .pos "publish", .pos "remove"]
  rules := [
    -- r0: =>O ~use
    ⟨"r0", .defeasible, .prescriptive, [], [.neg "use"]⟩,
    -- r1: license ~>O use
    ⟨"r1", .defeater, .prescriptive, [.plain (.pos "license")], [.pos "use"]⟩,
    -- r2: =>O ~publish * remove
    ⟨"r2", .defeasible, .prescriptive, [], [.neg "publish", .pos "remove"]⟩,
    -- r2e: approval ~>O publish
    ⟨"r2e", .defeater, .prescriptive, [.plain (.pos "approval")], [.pos "publish"]⟩,
    -- r3: =>O ~comment
    ⟨"r3", .defeasible, .prescriptive, [], [.neg "comment"]⟩,
    -- r3e: P(publish) ~>O comment
    ⟨"r3e", .defeater, .prescriptive,
      [.deontic ⟨.P, .pos "publish"⟩], [.pos "comment"]⟩,
    -- r4: commission =>O publish
    ⟨"r4", .defeasible, .prescriptive, [.plain (.pos "commission")], [.pos "publish"]⟩,
    -- r4x: commission =>O use
    ⟨"r4x", .defeasible, .prescriptive, [.plain (.pos "commission")], [.pos "use"]⟩,
    -- r5: bot =>O ~use
    ⟨"r5", .defeasible, .prescriptive, [.plain (.pos "bot")], [.neg "use"]⟩
  ]
  superiority := [
    ("r1", "r0"), ("r4x", "r0"), ("r5", "r1"), ("r5", "r4x"),
    ("r2e", "r2"), ("r3e", "r3")
  ]

-- Scenario B: license + publish (no approval, no removal — non-compensable)
def ex1TheoryB : Theory := { ex1Theory with
  facts := [.pos "license", .pos "publish"] }

-- Scenario C: license + commission
def ex1TheoryC : Theory := { ex1Theory with
  facts := [.pos "license", .pos "commission"] }

-- ── Example 3 & 4: TCPC 2012 complaint (§3.1) ─────────────────────────────────
-- Scenario: ExpressionDissatisfaction + InformationCall, AdviseComplaint absent

def ex3Theory : Theory where
  facts := [.pos "ExpressionDissatisfaction", .pos "InformationCall"]
  rules := [
    ⟨"tcpc1", .defeasible, .constitutive,
      [.plain (.pos "ExpressionDissatisfaction")], [.pos "complaint"]⟩,
    ⟨"tcpc2", .defeasible, .constitutive,
      [.plain (.pos "InformationCall")], [.neg "complaint"]⟩,
    ⟨"tcpc3", .defeater, .constitutive,
      [.plain (.pos "ProblemCall"), .plain (.pos "FirstCall")], [.pos "complaint"]⟩,
    ⟨"tcpc4", .defeasible, .constitutive,
      [.plain (.pos "AdviseComplaint")], [.pos "complaint"]⟩
  ]
  superiority := [("tcpc2", "tcpc1"), ("tcpc4", "tcpc2")]

-- With AdviseComplaint (Example 4 reversal)
def ex4Theory : Theory := { ex3Theory with
  facts := ex3Theory.facts ++ [.pos "AdviseComplaint"] }

-- ── Evaluation ────────────────────────────────────────────────────────────────

#eval do
  IO.println "=== Example 1A: license + publish + remove ==="
  let ext := computeExtension ex1Theory
  IO.println (renderQueryResults ["use", "publish", "comment"] ext)
  IO.println s!"  violation: {ext.hasViolation}"
  IO.println s!"  unresolved: {ext.unresolvedConflicts.length}"

#eval do
  IO.println "=== Example 1B: license + publish (no removal) ==="
  let ext := computeExtension ex1TheoryB
  IO.println (renderQueryResults ["use", "publish", "comment"] ext)
  IO.println s!"  violation: {ext.hasViolation}"
  IO.println s!"  unresolved: {ext.unresolvedConflicts.length}"

#eval do
  IO.println "=== Example 1C: license + commission ==="
  let ext := computeExtension ex1TheoryC
  IO.println (renderQueryResults ["use", "publish", "comment"] ext)
  IO.println s!"  violation: {ext.hasViolation}"
  if ext.hasUnresolvedConflicts then
    IO.println (renderUnresolvedConflicts ext)

#eval do
  IO.println "=== Example 3: ExpressionDissatisfaction + InformationCall ==="
  let ext := computeExtension ex3Theory
  IO.println (renderQueryResults ["complaint"] ext)

#eval do
  IO.println "=== Example 4: + AdviseComplaint ==="
  let ext := computeExtension ex4Theory
  IO.println (renderQueryResults ["complaint"] ext)

-- ── Abduction: which facts make a goal hold? ──────────────────────────────────
-- NDA confidentiality clause (cf. examples/other.ddl): default prohibition on
-- disclosure, with a permission carve-out gated on three conditions.

def ndaTheory : Theory where
  facts := []
  rules := [
    ⟨"def1", .defeasible, .constitutive, [.plain (.pos "Director")], [.pos "Representative"]⟩,
    ⟨"rprohibit", .defeasible, .prescriptive, [], [.neg "Disclose"]⟩,
    ⟨"rperm", .defeater, .prescriptive,
      [.plain (.pos "Representative"), .plain (.pos "NeedToKnow"), .plain (.pos "TransactionPurpose")],
      [.pos "Disclose"]⟩,
    ⟨"rcare", .defeasible, .prescriptive, [], [.pos "Protect"]⟩
  ]
  superiority := [("rperm", "rprohibit")]

-- Goal shorthands
private def gP   (a : Atom) : Condition := ⟨true,  true, .P, .pos a⟩
private def gF   (a : Atom) : Condition := ⟨true,  true, .O, .neg a⟩  -- F(a) = O(~a)
private def gNotO (a : Atom) : Condition := ⟨false, true, .O, .pos a⟩ -- ¬ O(a)

-- Goal/condition token parsing
#guard (parseCondition "P(Disclose)").toOption == some ⟨true,  true, .P, .pos "Disclose"⟩
#guard (parseCondition "F(Disclose)").toOption == some ⟨true,  true, .O, .neg "Disclose"⟩
#guard (parseCondition "O(~use)").toOption     == some ⟨true,  true, .O, .neg "use"⟩
#guard (parseCondition "!C(Notify)").toOption  == some ⟨false, true, .C, .pos "Notify"⟩
#guard (parseCondition "~complaint").toOption  == some ⟨true,  true, .C, .neg "complaint"⟩
#guard (parseAssumption "NeedToKnow").toOption == some (.factPos "NeedToKnow")
#guard (parseAssumption "~Knows").toOption     == some (.factNeg "Knows")
#guard (parseAssumption "-Knows").toOption     == some (.absent  "Knows")

-- Allowing Disclose requires exactly the three carve-out facts asserted directly.
#guard (abduce ndaTheory [] [gP "Disclose"]).minimal ==
  [[.pos "Representative", .pos "NeedToKnow", .pos "TransactionPurpose"]]

-- By default (no facts) disclosure is forbidden.
#guard (abduce ndaTheory [] [gF "Disclose"]).minimal == [[]]

-- "without asserting Representative directly": the constitutive def1 (Director ⇒
-- Representative) does not feed rperm's plain antecedent, so no config works.
#guard (abduce ndaTheory [.absent "Representative"] [gP "Disclose"]).minimal == []

-- Disclose allowed *and* Protect not obligated is impossible (rcare always fires).
#guard (abduce ndaTheory [] [gP "Disclose", gNotO "Protect"]).minimal == []

-- License: an obligation to `use` is reachable only by asserting `commission`.
#guard (abduce ex1Theory [] [⟨true, true, .O, .pos "use"⟩]).minimal == [[.pos "commission"]]

#eval do
  IO.println "=== Abduction: configurations that ALLOW Disclose ==="
  IO.println (renderAbduceResult (abduce ndaTheory [] [gP "Disclose"]) true 8)
  IO.println ""
  IO.println "=== Abduction: configurations that REQUIRE use (license) ==="
  IO.println (renderAbduceResult (abduce ex1Theory [] [⟨true, true, .O, .pos "use"⟩]) true 8)

-- ── Atom descriptions / provenance ────────────────────────────────────────────

private def describedSrc : String :=
  "atom Disclose: disclose CI to a third party | NDA s1\n" ++
  "atom PriorWrittenPermission: rights-holder gave prior written permission\n" ++
  "no_disclosure: =>O ~Disclose\n" ++
  "with_permission: PriorWrittenPermission ~>O Disclose\n" ++
  "superiority: with_permission > no_disclosure"

-- Descriptions parse; bare provenance text is captured as a quote; provenance
-- is optional.
#guard match Deontic.Parser.parse describedSrc with
  | .ok thy =>
    thy.atomDecl? "Disclose"
         == some ⟨"Disclose", "disclose CI to a third party", some { quote := some "NDA s1" }⟩
    && thy.atomDecl? "PriorWrittenPermission"
         == some ⟨"PriorWrittenPermission", "rights-holder gave prior written permission", none⟩
    && thy.undescribedAtoms == []
  | .error _ => false

-- A `uri:` keeps its GitHub-style `#L` selector verbatim on atom lines.
#guard match Deontic.Parser.parse "atom a: an atom | uri: docs/x.md#L3-L5\nr: a => b\natom b: another" with
  | .ok thy => (thy.atomDecl? "a").bind (·.provenance) == some { uri := some "docs/x.md#L3-L5" }
  | .error _ => false

-- A provenance uri must point to a markdown file.
#guard match Deontic.Parser.parse "atom a: an atom | uri: docs/x.txt" with
  | .error _ => true
  | .ok _    => false

-- Undescribed atoms are reported.
#guard match Deontic.Parser.parse "r: a => b" with
  | .ok thy => thy.undescribedAtoms == ["a", "b"]
  | .error _ => false

-- A declaration with no description is a parse error.
#guard match Deontic.Parser.parse "atom X:" with
  | .error _ => true
  | .ok _    => false

-- A `|` with nothing usable after it is a parse error.
#guard match Deontic.Parser.parse "atom X: a desc |" with
  | .error _ => true
  | .ok _    => false

#eval do
  IO.println "=== Atom dictionary ==="
  match Deontic.Parser.parse describedSrc with
  | .ok thy => IO.println (renderAtoms thy (fun _ => none))
  | .error e => IO.println s!"parse error: {e}"

-- ── Imports / namespacing ─────────────────────────────────────────────────────

-- Import directives are recorded by the (pure) parser; the loader resolves them.
#guard match Deontic.Parser.parse "from defs.ddl import *\nimport roles.ddl as r\natom a: d\nx: a => b\natom b: e" with
  | .ok thy => thy.imports == [.glob "defs.ddl", .namespaced "roles.ddl" "r"]
  | .error _ => false

-- Namespacing prefixes every atom and rule label.
#guard match Deontic.Parser.parse "atom a: d\nx: a => b\natom b: e" with
  | .ok thy =>
    let ns := thy.namespaced "m"
    ns.herbrandBase == ["m.a", "m.b"] && ns.rules.map (·.label) == ["m.x"]
  | .error _ => false

-- A merge fails when two declarations of the same atom disagree on description.
#guard match Deontic.Parser.parse "atom a: ONE\nx: a => b\natom b: e",
             Deontic.Parser.parse "atom a: TWO\ny: a => c\natom c: f" with
  | .ok t1, .ok t2 => (t1.mergeGuarded t2).toOption.isNone
  | _, _ => false

-- …and succeeds (deduping the shared atom) when the descriptions agree.
#guard match Deontic.Parser.parse "atom a: same\nx: a => b\natom b: e",
             Deontic.Parser.parse "atom a: same\ny: a => c\natom c: f" with
  | .ok t1, .ok t2 => match t1.mergeGuarded t2 with
    | .ok m => m.rules.length == 2 && m.atoms.length == 3
    | .error _ => false
  | _, _ => false
