#!/usr/bin/env bash
# Regression checks for the EIR 2004 formalization. Run from the repo root.
set -u
BIN=./.lake/build/bin/deontic
DDL=examples/eir/eir.ddl
pass=0; fail=0

expect() { # expect <desc> <regex> <atoms...> -- <assume>
  local desc="$1" pattern="$2"; shift 2
  local atoms=() ; while [ "$1" != "--" ]; do atoms+=("$1"); shift; done; shift
  local out
  out=$("$BIN" query "$DDL" "${atoms[@]}" --assume "$1" 2>&1)
  if grep -qE "$pattern" <<<"$out"; then
    pass=$((pass+1)); echo "ok   - $desc"
  else
    fail=$((fail+1)); echo "FAIL - $desc"; echo "$out" | sed 's/^/       /'
  fi
}

# reg 5(1) duty
expect "env request: must disclose"      'Disclose *: O\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo
expect "not environmental: no duty"      'Disclose *: P(w)?\(Disclose\)' Disclose -- Request,HoldsInfo
expect "not held (12(4)(a)): no duty"    'Disclose *: P(w)?\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo

# Every exception is qualified: engagement alone NEVER defeats the duty
expect "12(4)(b) engaged alone loses"    'Disclose *: O\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,ManifestlyUnreasonable
expect "12(4)(b) + PI maintains"         'Disclose *: F\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,ManifestlyUnreasonable,PiMaintainOutweighs
expect "12(4)(e) internal comms + PI"    'Disclose *: F\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,InternalCommunications,PiMaintainOutweighs
expect "12(5)(b) justice engaged alone loses" 'Disclose *: O\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,AdverseCourseOfJustice
expect "12(5)(b) + PI maintains"         'Disclose *: F\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,AdverseCourseOfJustice,PiMaintainOutweighs
expect "12(5)(e) commercial + PI"        'Disclose *: F\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,AdverseCommercialConfidentiality,PiMaintainOutweighs
expect "12(5)(g) env protection + PI"    'Disclose *: F\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,AdverseEnvironmentProtection,PiMaintainOutweighs

# reg 5(3): applicant's own data blocks the duty (P, not F)
expect "reg5(3) own data blocks duty"    'Disclose *: P(w)?\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,ApplicantOwnData

# reg 13 first condition needs no PI balance
expect "reg13 personal data first condition" 'Disclose *: F\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,ThirdPartyPersonalData,ContraveneDPPrinciples
expect "reg13 needs DP contravention"    'Disclose *: O\(Disclose\)' Disclose -- Request,IsEnvironmentalInfo,HoldsInfo,ThirdPartyPersonalData

# reg 14 refusal notice chains off the prohibition
expect "refusal triggers reg14 notice"   'RefusalNotice *: O\(RefusalNotice\)' RefusalNotice -- Request,IsEnvironmentalInfo,HoldsInfo,InternalCommunications,PiMaintainOutweighs

echo "----"
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
