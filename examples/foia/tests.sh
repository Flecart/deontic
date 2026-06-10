#!/usr/bin/env bash
# Regression checks for the FOIA pilot formalization. Mirrors the
# codice_penale/tests.sh pattern: run the enforcing load via `query`,
# grep for the expected status. Run from the repo root.
set -u
BIN=./.lake/build/bin/deontic
DDL=examples/foia/foia.ddl
pass=0; fail=0

expect() { # expect <desc> <atom-status-regex> <atoms...> -- <assume>
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

# s1 duties fire on a bare request
expect "bare request: must disclose"      'Disclose *: O\(Disclose\)'           Disclose -- Request,HoldsInfo
expect "bare request: must confirm"       'ConfirmOrDeny *: O\(ConfirmOrDeny\)' ConfirmOrDeny -- Request

# Absolute exemptions defeat the duty on engagement alone
expect "s21 absolute"                     'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsInfo,AccessibleOtherMeans
expect "s40(1) absolute"                  'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsInfo,ApplicantOwnData
expect "s40(2) absolute (first condition)" 'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsInfo,ThirdPartyPersonalData,ContraveneDPPrinciples
expect "s40(2) needs DP contravention"    'Disclose *: O\(Disclose\)' Disclose -- Request,HoldsInfo,ThirdPartyPersonalData

# Qualified exemptions need engagement AND the PI balance
expect "s43(2) engaged + PI maintain"     'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsInfo,PrejudiceCommercialInterests,PiMaintainOutweighs
expect "s43(2) engaged, PI favours disclosure" 'Disclose *: O\(Disclose\)' Disclose -- Request,HoldsInfo,PrejudiceCommercialInterests
expect "s42 engaged + PI maintain"        'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsInfo,LegalPrivilege,PiMaintainOutweighs
expect "s31 engaged + PI maintain"        'Disclose *: F\(Disclose\)' Disclose -- Request,HoldsInfo,PrejudiceLawEnforcement,PiMaintainOutweighs
expect "PI alone exempts nothing"         'Disclose *: O\(Disclose\)' Disclose -- Request,HoldsInfo,PiMaintainOutweighs

# NCND stacking
expect "s40(5A) NCND"                     'ConfirmOrDeny *: F\(ConfirmOrDeny\)' ConfirmOrDeny -- Request,ApplicantOwnData
expect "s31(3) NCND"                      'ConfirmOrDeny *: F\(ConfirmOrDeny\)' ConfirmOrDeny -- Request,ConfirmPrejudiceLawEnforcement,PiNcndMaintainOutweighs
expect "s31(3) NCND needs its PI balance" 'ConfirmOrDeny *: O\(ConfirmOrDeny\)' ConfirmOrDeny -- Request,ConfirmPrejudiceLawEnforcement

# s17 refusal notice chains off the derived prohibition
expect "withholding triggers s17 notice"  'RefusalNotice *: O\(RefusalNotice\)' RefusalNotice -- Request,HoldsInfo,AccessibleOtherMeans
expect "no withholding, no s17 duty"      'RefusalNotice *: P(w)?\(RefusalNotice\)' RefusalNotice -- Request,HoldsInfo

echo "----"
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
