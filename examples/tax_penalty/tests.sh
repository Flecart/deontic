#!/usr/bin/env bash
set -u
BIN=./.lake/build/bin/deontic
DDL=examples/tax_penalty/tax_penalty.ddl
pass=0; fail=0
expect() { local desc="$1" pattern="$2"; shift 2
  local atoms=(); while [ "$1" != "--" ]; do atoms+=("$1"); shift; done; shift
  local out; out=$("$BIN" query "$DDL" "${atoms[@]}" --assume "$1" 2>&1)
  if grep -qE "$pattern" <<<"$out"; then pass=$((pass+1)); echo "ok   - $desc"
  else fail=$((fail+1)); echo "FAIL - $desc"; echo "$out" | sed 's/^/       /'; fi }

expect "late return: penalty payable"      'PayPenalty *: O\(PayPenalty\)' PayPenalty -- FilingObligationNotified,ReturnLate,PenaltyAssessedNotified
expect "no notice to file: no duty"        'PayPenalty *: P(w)?\(PayPenalty\)' PayPenalty -- ReturnLate,PenaltyAssessedNotified
expect "return on time: no duty"           'PayPenalty *: P(w)?\(PayPenalty\)' PayPenalty -- FilingObligationNotified,PenaltyAssessedNotified
expect "invalid assessment: no duty"       'PayPenalty *: P(w)?\(PayPenalty\)' PayPenalty -- FilingObligationNotified,ReturnLate
expect "reasonable excuse blocks penalty"  'PayPenalty *: P(w)?\(PayPenalty\)' PayPenalty -- FilingObligationNotified,ReturnLate,PenaltyAssessedNotified,ReasonableExcuse,ExcuseRemediedPromptly
expect "excuse without prompt remedy fails" 'PayPenalty *: O\(PayPenalty\)' PayPenalty -- FilingObligationNotified,ReturnLate,PenaltyAssessedNotified,ReasonableExcuse
expect "special circumstances block"       'PayPenalty *: P(w)?\(PayPenalty\)' PayPenalty -- FilingObligationNotified,ReturnLate,PenaltyAssessedNotified,SpecialCircumstances
echo "----"; echo "$pass passed, $fail failed"; [ "$fail" -eq 0 ]
