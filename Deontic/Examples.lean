import Deontic.Theory
import Deontic.Extension
import Deontic.Query
import Deontic.Abduce
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
