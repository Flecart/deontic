import Deontic.Theory
import Deontic.Extension
import Deontic.Query
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
