#!/usr/bin/env bash
set -u
BIN=./.lake/build/bin/deontic
DDL=examples/employment/employment.ddl
pass=0; fail=0
expect() { local desc="$1" pattern="$2"; shift 2
  local atoms=(); while [ "$1" != "--" ]; do atoms+=("$1"); shift; done; shift
  local out; out=$("$BIN" query "$DDL" "${atoms[@]}" --assume "$1" 2>&1)
  if grep -qE "$pattern" <<<"$out"; then pass=$((pass+1)); echo "ok   - $desc"
  else fail=$((fail+1)); echo "FAIL - $desc"; echo "$out" | sed 's/^/       /'; fi }

expect "qualifying dismissal default unfair"  'FindUnfair *: O\(FindUnfair\)' FindUnfair -- Dismissed,QualifyingService
expect "no dismissal: no claim"               'FindUnfair *: P(w)?\(FindUnfair\)' FindUnfair -- QualifyingService
expect "short service, ordinary reason: no claim" 'FindUnfair *: P(w)?\(FindUnfair\)' FindUnfair -- Dismissed
expect "fair reason alone insufficient"       'FindUnfair *: O\(FindUnfair\)' FindUnfair -- Dismissed,QualifyingService,FairReasonShown
expect "reasonableness alone insufficient"    'FindUnfair *: O\(FindUnfair\)' FindUnfair -- Dismissed,QualifyingService,ReasonableResponse
expect "full s98 defence: claim fails"        'FindUnfair *: P(w)?\(FindUnfair\)' FindUnfair -- Dismissed,QualifyingService,FairReasonShown,ReasonableResponse
expect "auto-unfair beats the defence"        'FindUnfair *: O\(FindUnfair\)' FindUnfair -- Dismissed,AutomaticallyUnfairReason,FairReasonShown,ReasonableResponse
expect "auto-unfair needs no qualifying period" 'FindUnfair *: O\(FindUnfair\)' FindUnfair -- Dismissed,AutomaticallyUnfairReason
echo "----"; echo "$pass passed, $fail failed"; [ "$fail" -eq 0 ]
