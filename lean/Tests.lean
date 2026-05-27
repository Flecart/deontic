/-
Test runner: ports the Python `tests/` acceptance suite to Lean and reproduces
the paper's worked examples. Exits non-zero if any check fails.

Run with:  lake exe ddltest
-/
import Ddl
open Ddl

abbrev Check := String × Bool

def ext (src : String) : Extension := extension (parse! src)
def reasoner (src : String) : Reasoner := Reasoner.ofTheory (parse! src)

-- =====================================================================
-- Shared theories (verbatim from the paper / Python tests)
-- =====================================================================
def licenseRules : String := "
  r0:  =>O -use
  r1:  license ~>O use
  r2:  =>O -publish (x) remove
  r2e: approval ~>O publish
  r3:  =>O -comment
  r3e: P publish ~>O comment
  r4:  commission =>O publish
  r4x: commission =>O use
  r5:  bottom =>O -use
  r0 < r1
  r0 < r4x
  r1 < r5
  r4x < r2e
  r2 < r2e
  r3 < r3e
"

def complaintTheory : String := "
  tcpc1: ExpressionDissatisfaction => Complaint
  tcpc2: InformationCall           => -Complaint
  tcpc3: ProblemCall, FirstCall    ~> Complaint
  tcpc4: AdviseComplaint           => Complaint
  tcpc1 < tcpc2
  tcpc2 < tcpc4
"

def uturnTheory : String := "
  arr40a: AtTrafficLights    =>O -Uturn
  arr40e: UturnPermittedSign ~>O Uturn
  arr40a < arr40e
"

def premiumTheory : String := "
  c31:  highSpend       => premiumCustomer
  c32a: specialOrder    => surcharge
  c32b: premiumCustomer => -surcharge
  c32a < c32b
"

def chainRule : String := "r: =>O a (x) b (x) c\n"

-- =====================================================================
-- Basic defeasible logic (Governatori 2018, sect. 3.1)
-- =====================================================================
def basicChecks : List Check :=
  let e1 := ext "a."
  let e2 := ext "a.\nr1: a => b\nr2: b => c"
  let e3 := ext "r1: a => b"
  let e4 := ext "r1: => p\nr2: => -p"
  let e5 := ext "r1: => p\nr2: => -p\nr2 < r1"
  let e6 := ext "a. b. c.\nr1: a => p\nr2: b => p\nr3: c => -p\nr3 < r1"
  let e7 := ext "x.\nr1: x ~> p"
  let e8 := ext "x. y.\nr1: x => -p\nr2: y ~> p\nr1 < r2"
  let e9 := ext "r1: b => a\nr2: a => b"
  let e10 := ext "r3: => c\nr4: a => -c\nr1: b => a\nr2: a => b"
  [ ("fact_is_provable", e1.provable (lit "a") && e1.refuted (lit "a" true)),
    ("simple_chain", e2.provable (lit "b") && e2.provable (lit "c")),
    ("rule_not_fired", e3.refuted (lit "a") && e3.refuted (lit "b")),
    ("unresolved_conflict_blocks_both",
      !e4.provable (lit "p") && !e4.provable (lit "p" true) &&
      e4.refuted (lit "p") && e4.refuted (lit "p" true)),
    ("superiority_resolves", e5.provable (lit "p") && e5.refuted (lit "p" true)),
    ("team_defeat", e6.provable (lit "p") && e6.refuted (lit "p" true)),
    ("defeater_only_blocks", !e7.provable (lit "p") && e7.refuted (lit "p")),
    ("defeater_blocks_opposing", !e8.provable (lit "p" true) && !e8.provable (lit "p")),
    ("positive_cycle_refuted", e9.refuted (lit "a") && e9.refuted (lit "b")),
    ("cycle_attacker_unblocks", e10.refuted (lit "a") && e10.provable (lit "c")) ]

-- =====================================================================
-- Example 1 / Section 4: product-evaluation licence
-- =====================================================================
def licenseChecks : List Check :=
  let a := ext (licenseRules ++ "\nlicense. publish. remove.")
  let b := ext (licenseRules ++ "\nlicense. publish. remove. comment.")
  let c := ext (licenseRules ++ "\nlicense. publish. remove. comment. approval.")
  [ ("a_published_then_removed",
      a.forbidden (lit "publish") && a.obligation (lit "remove") &&
      !a.noncompliant && a.permitted (lit "use")),
    ("b_tweet_without_approval_noncompliant",
      b.forbidden (lit "publish") && !b.permitted (lit "publish") &&
      b.forbidden (lit "comment") && b.noncompliant &&
      b.forbidden (lit "use") && !b.permitted (lit "use")),
    ("c_tweet_after_approval_compliant",
      c.permitted (lit "publish") && !c.forbidden (lit "comment") &&
      c.permitted (lit "comment") && !c.noncompliant && c.permitted (lit "use")) ]

-- =====================================================================
-- Compensatory (contrary-to-duty) obligations + non-compliance
-- =====================================================================
def compensatoryChecks : List Check :=
  let e1 := ext (chainRule ++ "a.")
  let e2 := ext (chainRule ++ "-a.")
  let e3 := ext (chainRule ++ "-a. -b.")
  let e4 := ext (chainRule ++ "-a. -b. -c.")
  let e5 := ext "r: =>O a (x) b (x) a\n-a. -b."
  [ ("primary_only_when_complied",
      e1.obligation (lit "a") && !e1.obligation (lit "b") &&
      !e1.obligation (lit "c") && !e1.noncompliant),
    ("violation_triggers_compensation",
      e2.obligation (lit "a") && e2.obligation (lit "b") &&
      !e2.obligation (lit "c") && !e2.noncompliant),
    ("chained_compensation",
      e3.obligation (lit "a") && e3.obligation (lit "b") &&
      e3.obligation (lit "c") && !e3.noncompliant),
    ("non_compensable_violation", e4.obligation (lit "c") && e4.noncompliant),
    ("otimes_duplication_contraction",
      e5.obligation (lit "a") && e5.obligation (lit "b") && e5.noncompliant) ]

-- =====================================================================
-- Example 3/4: TCPC complaint
-- =====================================================================
def complaintChecks : List Check :=
  let e1 := ext (complaintTheory ++ "\nExpressionDissatisfaction. InformationCall.")
  let e2 := ext (complaintTheory ++ "\nExpressionDissatisfaction. InformationCall. AdviseComplaint.")
  [ ("information_call_not_a_complaint",
      e1.provable (lit "Complaint" true) && e1.refuted (lit "Complaint")),
    ("advise_complaint_reverses",
      e2.provable (lit "Complaint") && e2.refuted (lit "Complaint" true)) ]

-- =====================================================================
-- Example 5: U-turn (strong permission via permissive defeater)
-- =====================================================================
def uturnChecks : List Check :=
  let U := lit "Uturn"
  let e1 := ext (uturnTheory ++ "\nAtTrafficLights.")
  let e2 := ext (uturnTheory ++ "\nAtTrafficLights. UturnPermittedSign.")
  [ ("uturn_forbidden_at_lights",
      e1.forbidden U && !(e1.has "-" "O" U.complement) && !e1.strongPermitted U),
    ("permitted_sign_derogates",
      !e2.forbidden U && e2.has "-" "O" U.complement &&
      e2.strongPermitted U && e2.permitted U && !e2.obligation U) ]

-- =====================================================================
-- Example 2: premium customer (constitutive fragment)
-- =====================================================================
def premiumChecks : List Check :=
  let e1 := ext (premiumTheory ++ "\nspecialOrder. highSpend.")
  let e2 := ext (premiumTheory ++ "\nspecialOrder.")
  [ ("premium_exempt_from_surcharge",
      e1.provable (lit "premiumCustomer") && e1.provable (lit "surcharge" true) &&
      e1.refuted (lit "surcharge")),
    ("non_premium_pays_surcharge",
      e2.refuted (lit "premiumCustomer") && e2.provable (lit "surcharge") &&
      e2.refuted (lit "surcharge" true)) ]

-- =====================================================================
-- Proposition 1 invariants (coherence / consistency / operator interactions)
-- =====================================================================
def prop1Holds (t : Theory) : Bool := Id.run do
  let e := extension t
  let lits := t.herbrandAtoms.flatMap (fun a => [lit a, lit a true])
  for q in lits do
    let nq := q.complement
    for mod in ["C", "O", "P", "Ps", "Pw"] do
      if e.has "+" mod q && e.has "-" mod q then return false
    for mod in ["O", "Ps"] do
      if e.has "+" mod q && e.has "+" mod nq then return false
      if e.has "+" mod q && !(e.has "-" mod nq) then return false
    if e.obligation q && e.strongPermitted nq then return false
    if e.obligation q then
      for mod in ["P", "Ps", "Pw"] do
        if !(e.has "+" mod q) then return false
    if e.weakPermitted q && !(e.has "-" "O" nq) then return false
  return true

def propertyChecks : List Check :=
  let prop1Theories : List (String × String) :=
    [ ("obligation", "=>O p"),
      ("prohibition", "=>O -p"),
      ("conflict_resolved", "r1: =>O p\nr2: =>O -p\nr2 < r1"),
      ("uturn", uturnTheory ++ "\nAtTrafficLights. UturnPermittedSign."),
      ("complaint", complaintTheory ++ "\nExpressionDissatisfaction. InformationCall."),
      ("premium", premiumTheory ++ "\nspecialOrder. highSpend.") ]
  let prop1 := prop1Theories.map (fun (n, src) => (s!"proposition1:{n}", prop1Holds (parse! src)))
  let eo := ext "=>O p"
  let ep := ext "=>O -p"
  let eu := ext "r1: =>O wearSeatbelt\ndrive."
  prop1 ++
  [ ("obligation_entails_permissions",
      eo.obligation (lit "p") && eo.strongPermitted (lit "p") &&
      eo.weakPermitted (lit "p") && eo.permitted (lit "p") && eo.has "-" "O" (lit "p" true)),
    ("prohibition_is_obligation_of_complement",
      ep.forbidden (lit "p") && ep.obligation (lit "p" true) && ep.has "-" "O" (lit "p")),
    ("weak_but_not_strong_when_unregulated",
      eu.weakPermitted (lit "drive") && !eu.strongPermitted (lit "drive") && eu.permitted (lit "drive")) ]

-- =====================================================================
-- High-level Reasoner / Verdict / parse_query facade
-- =====================================================================
def apiChecks : List Check :=
  let ru := reasoner (uturnTheory ++ "\nAtTrafficLights. UturnPermittedSign.")
  let rc := reasoner "tcpc1: Diss => Complaint\ntcpc2: Info => -Complaint\ntcpc4: Advise => Complaint\ntcpc1 < tcpc2\n tcpc2 < tcpc4\nDiss. Info. Advise."
  let rd := reasoner "r: =>O wearSeatbelt\ndrive."
  let rl := reasoner licenseRules
  let base := rl.withFacts [lit "license", lit "publish", lit "remove"]
  let appealed := rl.withFacts [lit "license", lit "publish", lit "remove", lit "comment"]
  let v := rc.queryStr "Complaint"
  [ ("parse_query_forms",
      parseQuery "+dO remove" == ⟨"+", "O", lit "remove"⟩ &&
      parseQuery "-dC publish" == ⟨"-", "C", lit "publish"⟩ &&
      parseQuery "O remove" == ⟨"+", "O", lit "remove"⟩ &&
      parseQuery "F publish" == ⟨"+", "O", lit "publish" true⟩ &&
      parseQuery "Ps use" == ⟨"+", "Ps", lit "use"⟩ &&
      parseQuery "publish" == ⟨"+", "C", lit "publish"⟩ &&
      parseQuery "noncompliant" == ⟨"+", "⊥", BOTTOM⟩),
    ("friendly_query_uturn",
      ru.holds "Ps Uturn" && !ru.holds "F Uturn" && (ru.queryStr "F Uturn").holds == false),
    ("verdict_has_trace", v.holds && v.trace.any (fun l => (Ddl.strIndexOf l "tcpc4").isSome)),
    ("out_of_base_weakly_permitted",
      rd.holds "Pw swim" && rd.holds "P swim" && !rd.holds "O swim" && !rd.holds "Ps swim"),
    ("what_if_extra_facts_flip",
      !(base.queryStr "noncompliant").holds && (appealed.queryStr "noncompliant").holds) ]

-- =====================================================================
-- LLM-facing JSON theory interface (round-tripping with the DSL)
-- =====================================================================
def licenseJson : String :=
  "{\"facts\":[\"license\",\"publish\",\"remove\",\"comment\"],
    \"rules\":[
      {\"id\":\"r0\",\"kind\":\"prescriptive\",\"then\":{\"forbidden\":\"use\"}},
      {\"id\":\"r1\",\"kind\":\"prescriptive\",\"strength\":\"defeater\",\"if\":[\"license\"],\"then\":{\"obligation\":[\"use\"]}},
      {\"id\":\"r2\",\"kind\":\"prescriptive\",\"then\":{\"obligation\":[\"-publish\",\"remove\"]}},
      {\"id\":\"r2e\",\"kind\":\"prescriptive\",\"strength\":\"defeater\",\"if\":[\"approval\"],\"then\":{\"obligation\":[\"publish\"]}},
      {\"id\":\"r3\",\"kind\":\"prescriptive\",\"then\":{\"forbidden\":\"comment\"}},
      {\"id\":\"r3e\",\"kind\":\"prescriptive\",\"strength\":\"defeater\",\"if\":[\"P publish\"],\"then\":{\"obligation\":[\"comment\"]}},
      {\"id\":\"r4\",\"kind\":\"prescriptive\",\"if\":[\"commission\"],\"then\":{\"obligation\":[\"publish\"]}},
      {\"id\":\"r4x\",\"kind\":\"prescriptive\",\"if\":[\"commission\"],\"then\":{\"obligation\":[\"use\"]}},
      {\"id\":\"r5\",\"kind\":\"prescriptive\",\"if\":[\"bottom\"],\"then\":{\"forbidden\":\"use\"}}],
    \"superiority\":[[\"r0\",\"r1\"],[\"r0\",\"r4x\"],[\"r1\",\"r5\"],[\"r4x\",\"r2e\"],[\"r2\",\"r2e\"],[\"r3\",\"r3e\"]]}"

def premiumJson : String :=
  "{\"facts\":[\"highSpend\",\"specialOrder\"],
    \"rules\":[
      {\"id\":\"c31\",\"if\":[\"highSpend\"],\"then\":{\"counts_as\":\"premium\"}},
      {\"id\":\"c32a\",\"if\":[\"specialOrder\"],\"then\":\"surcharge\"},
      {\"id\":\"c32b\",\"if\":[\"premium\"],\"then\":\"-surcharge\"}],
    \"superiority\":[[\"c32a\",\"c32b\"]]}"

def okT (r : Except String Theory) : Theory :=
  match r with | .ok t => t | .error e => panic! s!"json error: {e}"

def errContains (r : Except String Theory) (sub : String) : Bool :=
  match r with | .error e => (Ddl.strIndexOf e sub).isSome | .ok _ => false

def jsonChecks : List Check :=
  let dslT := (parse! licenseRules).withFacts (parse! "license. publish. remove. comment.").facts
  let jsT := okT (theoryFromJsonStr licenseJson)
  let ed := extension dslT
  let ej := extension jsT
  let prem := extension (okT (theoryFromJsonStr premiumJson))
  let chainT := okT (theoryFromJsonStr "{\"rules\":[{\"id\":\"r\",\"then\":{\"obligation\":[\"-publish\",\"remove\"]}}]}")
  let t1 := parse! "r1: a => b\nr2: =>O -x (x) y\na.\nr1 < r2"
  let t2 := okT (theoryFromJson (theoryToJson t1))
  let e1 := extension t1
  let e2 := extension t2
  [ ("json_matches_dsl_for_license",
      (ed.obligation (lit "publish" true) == ej.obligation (lit "publish" true)) &&
      (ed.obligation (lit "comment" true) == ej.obligation (lit "comment" true)) &&
      (ed.obligation (lit "use" true) == ej.obligation (lit "use" true)) &&
      ed.noncompliant && ej.noncompliant),
    ("json_constructs_expected_rules",
      prem.provable (lit "premium") && prem.provable (lit "surcharge" true)),
    ("json_obligation_chain",
      (chainT.rules.headD default).mode == "O" &&
      (chainT.rules.headD default).head == [lit "publish" true, lit "remove"]),
    ("roundtrip_dsl_json_dsl",
      (e1.obligation (lit "b") == e2.obligation (lit "b")) &&
      (e1.provable (lit "b") == e2.provable (lit "b")) &&
      (e1.obligation (lit "x" true) == e2.obligation (lit "x" true)) &&
      (e1.obligation (lit "y") == e2.obligation (lit "y"))),
    ("unknown_superiority_rule_errors",
      errContains (theoryFromJsonStr "{\"rules\":[{\"id\":\"r1\",\"then\":\"a\"}],\"superiority\":[[\"r1\",\"ghost\"]]}") "unknown rule"),
    ("missing_then_errors",
      errContains (theoryFromJsonStr "{\"rules\":[{\"id\":\"r1\",\"if\":[\"a\"]}]}") "missing 'then'") ]

-- =====================================================================
def allGroups : List (String × List Check) :=
  [ ("basic_defeasible", basicChecks),
    ("license", licenseChecks),
    ("compensatory", compensatoryChecks),
    ("complaint", complaintChecks),
    ("uturn", uturnChecks),
    ("premium", premiumChecks),
    ("properties", propertyChecks),
    ("api", apiChecks),
    ("json_io", jsonChecks) ]

def main : IO UInt32 := do
  let mut total := 0
  let mut failed := 0
  for (group, checks) in allGroups do
    for (name, ok) in checks do
      total := total + 1
      if ok then
        IO.println s!"  ok    {group} :: {name}"
      else
        failed := failed + 1
        IO.println s!"  FAIL  {group} :: {name}"
  IO.println ""
  IO.println s!"{total - failed}/{total} checks passed"
  if failed == 0 then
    IO.println "ALL TESTS PASSED"
    return 0
  else
    IO.println s!"{failed} CHECK(S) FAILED"
    return 1
