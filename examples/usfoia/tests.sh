#!/usr/bin/env bash
set -u
BIN=./.lake/build/bin/deontic
DDL=examples/usfoia/usfoia.ddl
pass=0; fail=0
expect() { local desc="$1" pattern="$2"; shift 2
  local atoms=(); while [ "$1" != "--" ]; do atoms+=("$1"); shift; done; shift
  local out; out=$("$BIN" query "$DDL" "${atoms[@]}" --assume "$1" 2>&1)
  if grep -qE "$pattern" <<<"$out"; then pass=$((pass+1)); echo "ok   - $desc"
  else fail=$((fail+1)); echo "FAIL - $desc"; echo "$out" | sed 's/^/       /'; fi }

expect "request for held records: disclose"      'Disclose *: O\(Disclose\)' Disclose -- Request,HoldsRecords
expect "no responsive records: no duty"          'Disclose *: P(w)?\(Disclose\)' Disclose -- Request
expect "b1 classified: mandatory bar"            'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsRecords,ProperlyClassified
expect "b3 statutory bar: mandatory"             'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsRecords,StatutoryBar
expect "b5 engaged alone loses (foreseeable harm)" 'Disclose *: O\(Disclose\)' Disclose -- Request,HoldsRecords,DeliberativePrivileged
expect "b5 + foreseeable harm withholds"         'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsRecords,DeliberativePrivileged,ForeseeableHarm
expect "b4 + harm withholds"                     'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsRecords,ConfidentialCommercial,ForeseeableHarm
expect "b6 + harm withholds"                     'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsRecords,UnwarrantedPrivacyInvasion,ForeseeableHarm
expect "b7 + harm withholds"                     'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsRecords,LawEnforcementHarm,ForeseeableHarm
expect "harm alone exempts nothing"              'Disclose *: O\(Disclose\)' Disclose -- Request,HoldsRecords,ForeseeableHarm
echo "----"; echo "$pass passed, $fail failed"; [ "$fail" -eq 0 ]
