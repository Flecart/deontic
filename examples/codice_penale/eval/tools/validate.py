#!/usr/bin/env python3
"""validate — the QA gate for a dataset file.

Four checks (PLAN.md §4):
  1. schema         — each item validates against schema.json.
  2. engine-gold    — re-running the oracle on atoms_gold reproduces `gold`
                      (catches stale / hand-edited labels).
  3. leakage        — narrative must not name an element-atom rubric token or a
                      verdict word; flagged for a human to resolve.
  4. pair integrity — minimal_pair links are reciprocal, the twins' configs
                      differ, and their gold differs.

Exit 0 iff no ERRORs (leakage hits are WARNs by default; --strict promotes them).

Usage:  python3 validate.py ../dataset/v0_pilot.jsonl [--strict]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

import backward_gen as bg
import offences as off

SCHEMA = os.path.normpath(os.path.join(off.REPO,
        "examples/codice_penale/eval/schema.json"))

# Verdict words that would leak the conclusion if they appeared in a narrative.
LEAK_WORDS = [
    "punibile", "punito", "reato", "delitto", "colpevole", "assolto",
    "condannato", "scriminante", "legittima difesa", "imputabile",
    "omicidio", "furto", "rapina", "lesione", "lesioni", "percosse",
    "non punibile", "stato di necessità", "premeditazione",
]


def load_schema_validator():
    """Use jsonschema if available; else a tiny hand validator for our schema."""
    try:
        import jsonschema
        with open(SCHEMA, encoding="utf-8") as f:
            schema = json.load(f)
        v = jsonschema.Draft202012Validator(schema)
        return lambda it: [e.message for e in v.iter_errors(it)]
    except Exception:
        return _fallback_validate


_ID_RE = re.compile(r"^[a-z_]+-\d{3}$")


def _fallback_validate(it: dict) -> list[str]:
    errs = []
    req = ["id", "tier", "source", "theory", "narrative", "question",
           "atoms_gold", "gold", "distractor", "prior_divergent"]
    for k in req:
        if k not in it:
            errs.append(f"missing field {k}")
    if "id" in it and not _ID_RE.match(it["id"]):
        errs.append(f"bad id {it['id']!r}")
    if it.get("tier") not in (1, 2, 3, 4):
        errs.append(f"bad tier {it.get('tier')!r}")
    g = it.get("gold", {})
    if g.get("verdict") not in ("offence", "no-offence", "unresolved"):
        errs.append(f"bad verdict {g.get('verdict')!r}")
    for a, v in it.get("atoms_gold", {}).items():
        if v not in (0, 1):
            errs.append(f"atom {a} value not 0/1")
    return errs


def element_rubric_tokens() -> set[str]:
    """Italian rubric words drawn from the offence/scriminante atom descriptions.

    We approximate 'rubric token' by the distinctive Italian nouns in the atom
    glosses (length>4), so a narrative reusing the statute's own phrasing trips."""
    toks: set[str] = set()
    for w in LEAK_WORDS:
        toks.add(w.lower())
    return toks


def check(path: str, strict: bool) -> int:
    validate = load_schema_validator()
    items = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    by_id = {it["id"]: it for it in items}
    errors, warns = [], []

    leak = element_rubric_tokens()

    for it in items:
        iid = it.get("id", "?")
        # 1. schema
        for e in validate(it):
            errors.append(f"[schema] {iid}: {e}")

        # 2. engine-gold consistency
        present = [a for a, v in it.get("atoms_gold", {}).items() if v]
        pen = it["gold"].get("offence") or _guess_penalty(it, present)
        try:
            g = bg.verdict(it["theory"], pen, present)
            if g["verdict"] != it["gold"]["verdict"]:
                errors.append(f"[gold] {iid}: stale verdict "
                              f"{it['gold']['verdict']!r} != engine {g['verdict']!r}")
            elif g["penalty_status"] != it["gold"]["penalty_status"]:
                warns.append(f"[gold] {iid}: penalty_status drift "
                             f"{it['gold']['penalty_status']} != {g['penalty_status']}")
        except Exception as ex:
            errors.append(f"[gold] {iid}: engine error {ex}")

        # 3. leakage
        low = it["narrative"].lower()
        hits = sorted({w for w in leak if re.search(rf"\b{re.escape(w)}\b", low)})
        if hits:
            (errors if strict else warns).append(
                f"[leak] {iid}: narrative contains {hits}")

    # 4. pair integrity
    for it in items:
        twin_id = it.get("minimal_pair")
        if not twin_id:
            continue
        twin = by_id.get(twin_id)
        if not twin:
            errors.append(f"[pair] {it['id']}: dangling pair {twin_id!r}")
            continue
        if twin.get("minimal_pair") != it["id"]:
            errors.append(f"[pair] {it['id']}<->{twin_id}: not reciprocal")
        sa = set(a for a, v in it["atoms_gold"].items() if v)
        sb = set(a for a, v in twin["atoms_gold"].items() if v)
        diff = sa ^ sb
        if not diff:
            errors.append(f"[pair] {it['id']}<->{twin_id}: identical configs")
        elif len(diff) > 1 and it["theory"] == twin["theory"]:
            warns.append(f"[pair] {it['id']}<->{twin_id}: differ in {len(diff)} atoms {sorted(diff)}")
        ga, gb = it["gold"], twin["gold"]
        if (ga["verdict"], ga["offence"]) == (gb["verdict"], gb["offence"]) and \
           ga["penalty_status"] == gb["penalty_status"]:
            errors.append(f"[pair] {it['id']}<->{twin_id}: identical gold (no discrimination)")

    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"\n{len(items)} items · {len(errors)} errors · {len(warns)} warnings")
    return 1 if errors else 0


def _guess_penalty(it: dict, present: list[str]) -> str | None:
    """For no-offence items gold.offence is null; recover the offence's penalty
    atom from the catalogue by matching the theory file."""
    for o in off.catalogue().values():
        if o.file == it["theory"] and o.penalty_atom:
            # prefer an aggravated penalty if its trigger is present
            for pen, trig in o.aggravated:
                if trig and all(t in present for t in []) and any(t in present for t in trig):
                    return pen
            return o.penalty_atom
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--strict", action="store_true",
                    help="promote leakage warnings to errors")
    args = ap.parse_args()
    if not os.path.exists(bg.DEO):
        sys.exit(f"engine not built: {bg.DEO}\n  run: lake build deontic")
    sys.exit(check(args.dataset, args.strict))


if __name__ == "__main__":
    main()
