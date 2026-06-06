#!/usr/bin/env python3
"""backward_gen — the oracle.  Engine verdict over an offence + a chosen config.

Methodology (work backwards): we *choose* which atoms are present, ask the
deontic engine for the verdict, and treat that verdict as the gold label.  The
calculus — not annotator opinion — is the source of truth, so the dataset
doubles as a regression suite for the encoded theory.

Public API:
    verdict(file, penalty_atom, present_atoms) -> dict   # the `gold` object
    item_stub(offence, config, **meta) -> dict           # everything but narrative

CLI:
    python3 backward_gen.py --selftest
    python3 backward_gen.py --file <f.ddl> --penalty <Atom> --assume a,b,c
    python3 backward_gen.py --stubs           # emit one stub per catalogue offence
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

import offences as off

DEO = os.path.join(off.REPO, ".lake", "build", "bin", "deontic")


def _run_query(file_abs: str, atoms: list[str], present: list[str]) -> dict:
    """Call the CLI `query … --json` and parse the leading JSON object.

    The JSON object is printed first; a human-readable violation report may
    follow on stdout, so we decode just the first object with raw_decode.
    """
    cmd = [DEO, "query", file_abs, *atoms]
    if present:
        cmd += ["--assume", ",".join(present)]
    cmd += ["--json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout
    start = out.find("{")
    if start < 0:
        raise RuntimeError(f"no JSON from engine:\n{res.stdout}\n{res.stderr}")
    obj, _ = json.JSONDecoder().raw_decode(out[start:])
    return obj


def _status_of(obj: dict, atom: str) -> str:
    node = obj.get(atom)
    if not node:
        return "unknown"
    return node.get("status", "unknown")


def verdict(file_rel: str, penalty_atom: str | None, present_atoms: list[str],
            hinge: str = "Sanziona") -> dict:
    """Compute the `gold` object for one config. Deterministic.

    verdict:
      offence    -> Sanziona is O(...)   (the offender ought to be punished)
      no-offence -> Sanziona is F(...) (a scriminante bars punishment) or
                    not O(...) (an element missing => no FattoTipico)
      unresolved -> the engine reports an unresolved obligation conflict
    """
    file_abs = os.path.join(off.REPO, file_rel)
    want = [hinge] + ([penalty_atom] if penalty_atom else [])
    obj = _run_query(file_abs, want, present_atoms)

    san = _status_of(obj, hinge)
    pen = _status_of(obj, penalty_atom) if penalty_atom else "n/a"

    if obj.get("hasUnresolvedConflicts"):
        v = "unresolved"
    elif san.startswith("O("):
        v = "offence"
    else:
        v = "no-offence"

    if v == "offence":
        decisive = f"all elements present; {hinge} obligated -> {pen}"
    elif san.startswith("F("):
        decisive = "punishment prohibited (scriminante / non-imputabilità)"
    elif v == "unresolved":
        decisive = "unresolved obligation conflict — a judge must decide"
    else:
        decisive = "a constitutive element is missing -> no typical fact"

    return {
        "verdict": v,
        "offence": penalty_atom if v == "offence" else None,
        "penalty_status": san,
        "decisive": decisive,
    }


def verdict_auto(file_rel: str, present_atoms: list[str],
                 candidate_penalties: list[str], hinge: str = "Sanziona") -> dict:
    """Like `verdict`, but the offence isn't known in advance: query the hinge plus
    every candidate penalty atom and pick whichever penalty is obligated. Used by
    the deontic arm, which grounds atoms and then asks the engine 'what reato?'."""
    file_abs = os.path.join(off.REPO, file_rel)
    obj = _run_query(file_abs, [hinge] + candidate_penalties, present_atoms)
    san = _status_of(obj, hinge)
    chosen = next((p for p in candidate_penalties
                   if _status_of(obj, p).startswith("O(")), None)
    if obj.get("hasUnresolvedConflicts"):
        v = "unresolved"
    elif san.startswith("O("):
        v = "offence"
    else:
        v = "no-offence"
    return {
        "verdict": v,
        "offence": chosen if v == "offence" else None,
        "penalty_status": san,
        "decisive": "",
    }


def item_stub(key: str, o: off.Offence, config: dict[str, int],
              seq: int, tier: int, **meta) -> dict:
    """A dataset item with everything BUT narrative/question (those are authored)."""
    present = [a for a, v in config.items() if v]
    g = verdict(o.file, o.penalty_atom, present)
    item = {
        "id": f"{o.name}-{seq:03d}",
        "tier": tier,
        "source": meta.get("source", "synthetic"),
        "theory": o.file,
        "narrative": meta.get("narrative", ""),
        "question": meta.get("question", "È punibile la persona descritta, e per quale reato?"),
        "atoms_gold": {a: int(bool(v)) for a, v in config.items()},
        "gold": g,
        "minimal_pair": meta.get("minimal_pair"),
        "distractor": meta.get("distractor", False),
        "prior_divergent": meta.get("prior_divergent", False),
    }
    return item


# --------------------------------------------------------------------------- #
# self-test: a handful of labels we know by hand (cf. tests.sh)               #
# --------------------------------------------------------------------------- #
SELFTESTS = [
    # (file, penalty, present, expected_verdict)
    ("examples/codice_penale/furto.ddl", "ReclusioneFurto",
     ["Impossessamento", "CosaMobileAltrui", "Sottrazione", "FineDiProfitto", "Querela"],
     "offence"),
    ("examples/codice_penale/furto.ddl", "ReclusioneFurto",
     ["Impossessamento", "CosaMobileAltrui", "Sottrazione", "Querela"],  # no FineDiProfitto
     "no-offence"),
    ("examples/codice_penale/omicidio.ddl", "Reclusione575",
     ["CagionaMorte", "Dolo"], "offence"),
    ("examples/codice_penale/omicidio.ddl", "Reclusione575",
     ["CagionaMorte", "Dolo", "PericoloAttuale", "DifesaProporzionata"],  # legittima difesa
     "no-offence"),
    ("examples/codice_penale/omicidio.ddl", "Reclusione575",
     ["CagionaMorte", "Dolo", "VizioTotaleMente", "Preordinato"],  # actio libera -> punibile
     "offence"),
    ("examples/codice_penale/omicidio.ddl", "Reclusione575",
     ["CagionaMorte", "Dolo", "MinoreAnni14"], "no-offence"),
]


def selftest() -> int:
    bad = 0
    for file, pen, present, want in SELFTESTS:
        g = verdict(file, pen, present)
        ok = g["verdict"] == want
        bad += not ok
        flag = "ok  " if ok else "FAIL"
        print(f"{flag} {os.path.basename(file):16} {want:11} got {g['verdict']:11} "
              f"[{g['penalty_status']}]  {','.join(present)}")
    print(f"\n{'ALL PASS' if not bad else f'{bad} FAILED'}")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--stubs", action="store_true", help="emit one base-config stub per offence")
    ap.add_argument("--file")
    ap.add_argument("--penalty")
    ap.add_argument("--assume", default="")
    args = ap.parse_args()

    if not os.path.exists(DEO):
        sys.exit(f"engine not built: {DEO}\n  run: lake build deontic")

    if args.selftest:
        sys.exit(selftest())
    if args.stubs:
        cat = off.catalogue()
        for i, (key, o) in enumerate(cat.items(), 1):
            stub = item_stub(key, o, o.base_config(), seq=i, tier=1)
            print(json.dumps(stub, ensure_ascii=False))
        return
    if args.file and args.penalty:
        present = [a for a in args.assume.split(",") if a]
        print(json.dumps(verdict(args.file, args.penalty, present),
                         ensure_ascii=False, indent=2))
        return
    ap.error("nothing to do: use --selftest, --stubs, or --file/--penalty/--assume")


if __name__ == "__main__":
    main()
