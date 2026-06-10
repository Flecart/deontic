#!/usr/bin/env python3
"""FOIA Phase-0 pipeline: engine vs OpenAI models on real FTT decisions.

Three arms per case, so accuracy can be attributed (grounding vs deduction):

  oracle  hand-verified facts -> deontic engine          (deduction ceiling)
  ground  LLM grounds atoms from the case background -> deontic engine
  llm     LLM decides everything directly                (no engine)

Each arm is scored on three dimensions against the tribunal gold:

  disposition  withhold / disclose            (the outcome)
  engagement   which exemption rules engage   (rule selection — the deduction-
               relevant signal; gold in the case file's `## Gold rules`)
  pi           the s2(2)(b) public-interest direction (maintain / disclose;
               scored only when the tribunal reached the balance)

"Engaged" means the exemption's own test is met (e.g. prejudice to commercial
interests); the PI balance is the separate s2(2)(b) limb, so it is scored
separately even though the DDL folds both into a qualified rule's body.

Cases live in cases/*.md (background = found facts only, no tribunal
conclusions). The theory is examples/foia/foia.ddl. Run from anywhere:

  python docs/experiments/foia_corpus/pipeline.py                      # oracle only
  python docs/experiments/foia_corpus/pipeline.py --arms oracle,ground,llm \
      --model gpt-4.1 -v

OpenAI arms need OPENAI_API_KEY and `pip install openai`.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))

from deontic_py import Deontic, status_code  # noqa: E402

DDL = REPO / "examples" / "foia" / "foia.ddl"
CASES_DIR = Path(__file__).resolve().parent / "cases"
RUNS_DIR = Path(__file__).resolve().parent / "runs"
DECISION_ATOM = "Disclose"
BEARER = "Authority"
PI_ATOM = "PiMaintainOutweighs"

# Rule label -> the atoms of its *own* test (the PI atom excluded: engagement
# and the s2(2)(b) balance are separate limbs). Mirrors foia.ddl. Includes the
# Part I duty blockers (s9/s12/s14) so rule-selection is scoreable for
# procedural outcomes too.
ENGAGEMENT: dict[str, list[str]] = {
    "s21_exempt": ["AccessibleOtherMeans"],
    "s22_exempt": ["IntendedFuturePublication"],
    "s22a_exempt": ["OngoingResearchProgramme"],
    "s23_exempt": ["SecurityBodyInfo"],
    "s24_exempt": ["SafeguardNationalSecurity"],
    "s26_exempt": ["PrejudiceDefence"],
    "s27_exempt": ["PrejudiceInternationalRelations"],
    "s28_exempt": ["PrejudiceUkRelations"],
    "s29_exempt": ["PrejudiceEconomy"],
    "s30_exempt": ["CriminalInvestigationInfo"],
    "s31_exempt": ["PrejudiceLawEnforcement"],
    "s32_exempt": ["CourtRecordInfo"],
    "s33_exempt": ["PrejudiceAuditFunctions"],
    "s34_exempt": ["ParliamentaryPrivilege"],
    "s35_exempt": ["GovernmentPolicyInfo"],
    "s36_exempt": ["QualifiedPersonOpinionPrejudice"],
    "s37_royal_exempt": ["RoyalSovereignCommunications"],
    "s37_other_exempt": ["RoyalOtherOrHonours"],
    "s38_exempt": ["EndangerHealthSafety"],
    "s39_exempt": ["EnvironmentalInfo"],
    "s40_1_exempt": ["ApplicantOwnData"],
    "s40_2_exempt": ["ThirdPartyPersonalData", "ContraveneDPPrinciples"],
    "s41_exempt": ["ActionableBreachConfidence"],
    "s42_exempt": ["LegalPrivilege"],
    "s43_1_exempt": ["TradeSecret"],
    "s43_2_exempt": ["PrejudiceCommercialInterests"],
    "s44_exempt": ["StatutoryProhibition"],
    "s12_cost": ["CostExceedsLimit"],
    "s14_vex": ["VexatiousRequest"],
    "s14_rep": ["RepeatedRequest"],
    "s9_fees": ["FeesNoticeUnpaid"],
}
# NCND rules (decision: confirm cases) — same shape, ConfirmOrDeny side.
NCND_ENGAGEMENT: dict[str, list[str]] = {
    "s23_ncnd": ["ConfirmWouldRevealSecurityBodyInfo"],
    "s24_ncnd": ["NcndRequiredNationalSecurity"],
    "s30_ncnd": ["ConfirmWouldRevealInvestigationInfo"],
    "s31_3_ncnd": ["ConfirmPrejudiceLawEnforcement"],
    "s40_5a_ncnd": ["ApplicantOwnData"],
    "sx_ncnd": ["ConfirmWouldCauseExemptHarm"],
    "s14_vex_ncnd": ["VexatiousRequest"],
    "s9_fees_ncnd": ["FeesNoticeUnpaid"],
}
PI_NCND_ATOM = "PiNcndMaintainOutweighs"
# Short codes the llm arm answers with (avoids leaking rule-label spelling).
EXEMPTION_CODES = {label.removesuffix("_exempt"): label for label in ENGAGEMENT}
EXEMPTION_CODES.update({label: label for label in NCND_ENGAGEMENT})
# Administrative-duty conclusions: real provisions (s10/s16) but never
# evidenced in case backgrounds — excluded from the facts-agreement universe
# so they don't inflate agreement with trivial mutual omissions.
NON_GROUNDABLE = {DECISION_ATOM, "RespondInTime", "AdviseAssist"}


# ── case files ──────────────────────────────────────────────────────────────

def load_case(path: Path) -> dict:
    """Parse a cases/*.md file. HTML comments are stripped *before* sectioning
    so gold rationale never reaches a prompt."""
    text = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.DOTALL)
    sections: dict[str, str] = {}
    current = "_head"
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = ""
        else:
            sections[current] = sections.get(current, "") + line + "\n"
    meta = dict(re.findall(r"^(\w+):[ \t]*(.+)$", sections["_head"], re.M))
    rules = dict(re.findall(r"^(\w+):[ \t]*(.*)$", sections.get("gold rules", ""), re.M))
    return {
        "name": path.stem,
        "citation": meta.get("citation", "?"),
        "verified": meta.get("verified", "no").strip().lower() == "yes",
        # "disclose" (default) or "confirm" — which s1 duty the case decides;
        # pure NCND disputes are scored on the ConfirmOrDeny atom.
        "decision": meta.get("decision", "disclose").strip().lower(),
        "background": sections.get("background", "").strip(),
        "disputed": sections.get("disputed information", "").strip(),
        "oracle_facts": _csv(sections.get("oracle facts", "")),
        "gold": {
            "disposition": sections.get("gold", "").strip().split()[0],
            "engaged": _csv(rules.get("engaged", "")),
            "pi": rules.get("pi", "na").strip(),
        },
    }


def _csv(s: str) -> list[str]:
    return [t.strip() for t in s.replace("\n", " ").split(",") if t.strip()]


# ── engine side ─────────────────────────────────────────────────────────────

def engine_result(d: Deontic, facts: list[str], verbose: bool,
                  decision: str = "disclose") -> dict:
    """Disposition / engagement / pi from a fact set, via the proof
    certificate. `decision` picks the duty in dispute: "disclose" (s1(1)(b),
    the default) or "confirm" (s1(1)(a) — pure NCND cases)."""
    atom = DECISION_ATOM if decision != "confirm" else "ConfirmOrDeny"
    pi_atom = PI_ATOM if decision != "confirm" else PI_NCND_ATOM
    engagement = ENGAGEMENT if decision != "confirm" else NCND_ENGAGEMENT
    rep = d.why(str(DDL), [atom], assume=facts)[atom][BEARER]
    code = status_code(rep.status)
    engaged = [lbl for lbl, atoms in engagement.items()
               if all(a in facts for a in atoms)]
    if verbose:
        win = ", ".join(rep.winning_rules) or "(none)"
        beaten = [f"{r.rule} by {','.join(r.defeated_by)}"
                  for r in rep.for_o + rep.against_o if r.defeated_by]
        print(f"    engine why     : {rep.status}; winning {win}"
              + (f"; defeated {'; '.join(beaten)}" if beaten else ""))
    # O = duty stands -> disclose. F = prohibition derived -> withhold.
    # P/Ps/Pw = the duty was BLOCKED (s9/s12/s14 defeater): the authority is
    # not obliged, so a refusal is upheld -> withhold.
    disposition = {"O": "disclose", "F": "withhold",
                   "P": "withhold", "Ps": "withhold", "Pw": "withhold",
                   }.get(code, f"unclear({code})")
    return {
        "disposition": disposition,
        "engaged": engaged,
        "pi": "maintain" if pi_atom in facts else "disclose",
    }


def atom_dictionary(d: Deontic) -> str:
    return "\n".join(f"- {e.atom}: {e.description}" for e in d.atoms(str(DDL)))


# ── atom-scoped precedents (examples/foia/precedents.md) ────────────────────

PRECEDENTS_MD = REPO / "examples" / "foia" / "precedents.md"


def load_precedents() -> dict[str, list[tuple[str, str]]]:
    """{atom: [(source_case_stem, note), ...]} from precedents.md."""
    if not PRECEDENTS_MD.exists():
        return {}
    out: dict[str, list[tuple[str, str]]] = {}
    atom = None
    source = None
    note_lines: list[str] = []

    def flush():
        if atom and source and note_lines:
            note = re.sub(r"\s+", " ", " ".join(note_lines)).strip()
            out.setdefault(atom, []).append((source, note.removeprefix("note:").strip()))

    for line in PRECEDENTS_MD.read_text().splitlines():
        if line.startswith("## "):
            flush(); atom, source, note_lines = line[3:].strip(), None, []
        elif line.startswith("- source:"):
            flush(); source = line.split(":", 1)[1].split("#")[0].strip(); note_lines = []
        elif source and line.strip():
            note_lines.append(line.strip())
        elif source and not line.strip() and note_lines:
            flush(); source = None; note_lines = []
    flush()
    return out


def precedent_lines(atom: str, case_name: str,
                    precedents: dict[str, list[tuple[str, str]]]) -> str:
    """The atom's precedent notes, LEAVE-ONE-OUT: a case never sees entries
    sourced from itself (Garrard parts share the garrard… stem prefix)."""
    notes = [note for src, note in precedents.get(atom, [])
             if not case_name.startswith(src)]
    return "".join(f"\n    precedent (from another case): {n}" for n in notes)


# ── run log (JSONL: every LLM call + every arm result, for post-hoc
#    analysis of WHY a fact was asserted/missed; see view_run.py) ────────────

_log_file: Path | None = None


def start_run(tag: str) -> Path:
    """Open a fresh JSONL run log; every subsequent log_event appends to it."""
    global _log_file
    RUNS_DIR.mkdir(exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    _log_file = RUNS_DIR / f"run_{stamp}_{tag}.jsonl"
    return _log_file


def log_event(record: dict) -> None:
    if _log_file is None:
        return
    record = {"ts": datetime.datetime.now().isoformat(timespec="seconds"),
              **record}
    with _log_file.open("a") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


# ── OpenAI side ─────────────────────────────────────────────────────────────

def call_openai(model: str, system: str, user: str,
                meta: dict | None = None) -> str:
    from openai import OpenAI  # lazy: only the API arms need it

    t0 = time.time()
    resp = OpenAI().chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
    )
    reply = resp.choices[0].message.content or ""
    usage = getattr(resp, "usage", None)
    log_event({
        "type": "llm_call",
        **(meta or {}),
        "model": model,
        "system": system,
        "user": user,
        "reply": reply,
        "seconds": round(time.time() - t0, 2),
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
    })
    return reply


def parse_json_reply(text: str) -> dict:
    """Tolerate code fences / prose around the JSON object."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON object in model reply:\n{text}")
    return json.loads(m.group(0))


GROUND_SYSTEM = """\
You are the fact-finder in a UK Freedom of Information Act 2000 appeal.
You are given (a) a dictionary of atoms, each with the exact meaning that
asserting it commits you to — the description IS the test: apply its stated
truth conditions, nothing else; and (b) the factual background of a real case.

Decide, for each atom, whether it HOLDS on the balance of the background.
Some atoms are evaluative (would disclosure prejudice X? would it contravene
the data protection principles? does the public interest in maintaining the
exemption outweigh disclosure?) — make the judgment a tribunal would make.

Hard rules:
- Base every judgment ONLY on the supplied background. If the background does
  not state evidence establishing an atom, the atom does not hold. NEVER rely
  on material you have not been shown (closed bundles, annexes, "the evidence
  shows") and never invent evidence.
- Include EVERY atom whose test is satisfied, including procedural ones (a
  request was made, a refusal notice was given), whether or not it seems
  determinative of the outcome. You are finding facts, not selecting the
  relevant ones.
- Where an atom carries interpretive precedents from OTHER cases, use them as
  guidance on how its test applies to fact patterns like this one.
- Do not invent atoms not in the dictionary.

Reply with ONLY a JSON object: {"facts": ["Atom", ...], "reasoning": "<brief,
one line per evaluative atom you included or deliberately excluded>"}"""

LLM_SYSTEM = """\
You are the First-tier Tribunal deciding a UK Freedom of Information Act 2000
appeal. Based on the factual background, decide:

1. which exemptions or duty-blockers are ENGAGED (their own test is met), from
   these codes:
   s21 (information accessible to the applicant by other means),
   s22 (held for intended future publication, reasonable to withhold until then),
   s22a (ongoing research programme pre-publication),
   s23 (supplied by or relates to the security bodies),
   s24 (withholding required to safeguard national security),
   s26 (prejudice to defence or armed forces),
   s27 (prejudice to international relations, or confidential foreign-state info),
   s28 (prejudice to relations between UK administrations),
   s29 (prejudice to the UK economy or an administration's finances),
   s30 (held for a criminal investigation/proceedings, or confidential sources),
   s31 (prejudice to law enforcement),
   s32 (held only as a court/inquiry/arbitration record),
   s33 (prejudice to the authority's audit functions over other bodies),
   s34 (parliamentary privilege),
   s35 (government policy formulation, ministerial communications, law officers),
   s36 (qualified person's reasonable opinion: prejudice to effective conduct
        of public affairs / inhibition of free and frank advice),
   s37_royal (communications with the Sovereign, heir, or second in line),
   s37_other (other royal communications, or honours),
   s38 (endanger any individual's health or safety),
   s39 (environmental information, handled under the environmental regime),
   s40_1 (applicant's own personal data),
   s40_2 (third-party personal data whose disclosure would contravene the
          data-protection principles),
   s41 (actionable breach of confidence over information obtained from another),
   s42 (legal professional privilege),
   s43_1 (trade secret),
   s43_2 (prejudice to commercial interests),
   s44 (disclosure prohibited by another enactment or contempt of court),
   s12_cost (cost of compliance exceeds the appropriate limit),
   s14_vex (vexatious request), s14_rep (repeated request),
   s9_fees (fees notice unpaid);
2. for a qualified exemption, the section 2(2)(b) public-interest balance:
   "maintain" (PI in maintaining the exemption outweighs disclosure),
   "disclose", or "na" if no qualified exemption is engaged;
3. the disposition: must the authority disclose the disputed information, or
   may it withhold (or decline to comply with) the request?

Reply with ONLY a JSON object:
{"engaged": ["s43_2", ...], "pi": "maintain" | "disclose" | "na",
 "disposition": "disclose" | "withhold", "reasoning": "<brief>"}"""


def run_ground_arm(d: Deontic, case: dict, model: str, verbose: bool,
                   atoms_per_call: int = 0, seed: int | None = None,
                   precedents: dict | None = None) -> dict:
    """Ground atoms from the background, in batches of `atoms_per_call`
    dictionary entries per API call (0 = all in one call, the default).

    The batch is the *design parameter*: it controls how many atoms the model
    judges simultaneously. Batches are INDEPENDENT calls over the same
    background — the case text itself carries the inter-atom context (e.g.
    which exemption is claimed), so no batch needs another batch's output.
    `seed` shuffles the atom order before batching (composition is otherwise
    dictionary order); report it with results.
    """
    # The decision atom is the question; admin-duty conclusions are never
    # evidenced in backgrounds — neither is groundable.
    entries = [e for e in d.atoms(str(DDL)) if e.atom not in NON_GROUNDABLE]
    if seed is not None:
        import random
        random.Random(seed).shuffle(entries)
    k = atoms_per_call if atoms_per_call > 0 else len(entries)
    batches = [entries[i:i + k] for i in range(0, len(entries), k)]

    known = {e.atom for e in entries}
    facts: list[str] = []
    dropped: list[str] = []
    for n, batch in enumerate(batches, 1):
        dictionary = "\n".join(
            f"- {e.atom}: {e.description}"
            + (precedent_lines(e.atom, case["name"], precedents)
               if precedents else "")
            for e in batch)
        user = (f"CASE BACKGROUND:\n{case['background']}\n\n"
                f"DISPUTED INFORMATION:\n{case['disputed']}\n\n"
                f"ATOM DICTIONARY (judge ONLY these atoms):\n{dictionary}\n\n")
        meta = {"case": case["name"], "arm": "ground", "batch": n,
                "batches": len(batches), "batch_atoms": sorted(e.atom for e in batch)}
        reply = parse_json_reply(call_openai(model, GROUND_SYSTEM, user, meta))
        batch_atoms = {e.atom for e in batch}
        got = [f for f in reply.get("facts", []) if f in batch_atoms]
        dropped += [f for f in reply.get("facts", []) if f not in batch_atoms]
        facts += got
        if verbose and len(batches) > 1:
            print(f"    batch {n}/{len(batches)} ({len(batch)} atoms) "
                  f"-> {', '.join(got) or '(none)'}")
        if verbose and len(batches) == 1:
            print(f"    grounded facts : {', '.join(got) or '(none)'}")
            print(f"    reasoning      : {reply.get('reasoning', '')}")
    if verbose and dropped:
        print(f"    dropped out-of-batch/unknown: {', '.join(dropped)}")

    res = engine_result(d, facts, verbose, case["decision"])
    # Per-atom grounding accuracy against the verified oracle facts — the
    # sensitive endpoint for the batch-size experiment (|universe| judgments
    # per case instead of one disposition).
    oracle = set(case["oracle_facts"])
    pred = set(facts)
    agree = [a for a in known if (a in pred) == (a in oracle)]
    res["facts_agreement"] = (len(agree), len(known),
                              sorted(oracle - pred), sorted(pred - oracle))
    return res


def run_llm_arm(case: dict, model: str, verbose: bool) -> dict:
    user = (f"CASE BACKGROUND:\n{case['background']}\n\n"
            f"DISPUTED INFORMATION:\n{case['disputed']}")
    meta = {"case": case["name"], "arm": "llm"}
    reply = parse_json_reply(call_openai(model, LLM_SYSTEM, user, meta))
    if verbose:
        print(f"    reasoning      : {reply.get('reasoning', '')}")
    engaged = [EXEMPTION_CODES[c] for c in reply.get("engaged", [])
               if c in EXEMPTION_CODES]
    return {
        "disposition": reply.get("disposition", "unclear"),
        "engaged": engaged,
        "pi": reply.get("pi", "na"),
    }


# ── scoring ─────────────────────────────────────────────────────────────────

DIMS = ("disposition", "engaged", "pi")


def score(pred: dict, gold: dict) -> dict[str, bool | None]:
    """Per-dimension hit; pi is None (unscored) when the tribunal never
    reached the balance (gold pi = na)."""
    return {
        "disposition": pred["disposition"] == gold["disposition"],
        "engaged": sorted(pred["engaged"]) == sorted(gold["engaged"]),
        "pi": None if gold["pi"] == "na" else pred["pi"] == gold["pi"],
    }


def fmt_dim(name: str, hit: bool | None, pred) -> str:
    mark = "--- " if hit is None else ("OK  " if hit else "MISS")
    shown = ", ".join(pred) if isinstance(pred, list) else pred
    return f"  [{mark}] {name:<12} -> {shown or '(none)'}"


# ── main ────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--case", action="append",
                    help="case name (stem of cases/*.md); repeatable; default all")
    ap.add_argument("--arms", default="oracle",
                    help="comma list of oracle,ground,llm (default: oracle)")
    ap.add_argument("--model", default="gpt-4.1",
                    help="OpenAI model for ground/llm arms (default: gpt-4.1)")
    ap.add_argument("--atoms-per-call", type=int, default=0, metavar="K",
                    help="ground arm: judge K atoms per API call "
                         "(0 = all at once, the default)")
    ap.add_argument("--seed", type=int, default=None,
                    help="shuffle atom order before batching (ground arm)")
    ap.add_argument("--precedents", action="store_true",
                    help="ground arm: attach each atom's interpretive "
                         "precedents (examples/foia/precedents.md), "
                         "leave-one-out by source case")
    ap.add_argument("--allow-unverified", action="store_true",
                    help="run cases whose labels a human has not verified")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="show grounded facts, why-certificates, model reasoning")
    args = ap.parse_args()

    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    if {"ground", "llm"} & set(arms) and not os.environ.get("OPENAI_API_KEY"):
        print("error: ground/llm arms need OPENAI_API_KEY", file=sys.stderr)
        return 2

    paths = ([CASES_DIR / f"{c}.md" for c in args.case]
             if args.case else sorted(CASES_DIR.glob("*.md")))
    d = Deontic(cache=True)

    precedents = load_precedents() if args.precedents else None

    log = start_run("-".join(arms))
    log_event({"type": "run_meta", "argv": sys.argv[1:], "arms": arms,
               "model": args.model, "atoms_per_call": args.atoms_per_call,
               "seed": args.seed, "precedents": bool(precedents),
               "cases": [p.stem for p in paths]})
    print(f"log: {log.relative_to(REPO)}")

    rows: list[tuple[str, dict]] = []  # (arm, hits)
    facts_scores: list[tuple[int, int]] = []  # ground arm: (agree, total)
    for path in paths:
        case = load_case(path)
        if not case["verified"] and not args.allow_unverified:
            print(f"\n=== {case['name']}: SKIPPED (verified: no — check labels "
                  "against the reasoning file, or pass --allow-unverified)")
            continue
        g = case["gold"]
        print(f"\n=== {case['name']}  ({case['citation']})"
              + ("" if case["verified"] else "  [UNVERIFIED LABELS]"))
        print(f"    gold: {g['disposition']}; engaged "
              f"{', '.join(g['engaged']) or '(none)'}; pi {g['pi']}")
        for arm in arms:
            if arm == "oracle":
                pred = engine_result(d, case["oracle_facts"], args.verbose,
                                     case["decision"])
            elif arm == "ground":
                pred = run_ground_arm(d, case, args.model, args.verbose,
                                      args.atoms_per_call, args.seed,
                                      precedents)
            elif arm == "llm":
                pred = run_llm_arm(case, args.model, args.verbose)
            else:
                print(f"  unknown arm '{arm}', skipping"); continue
            hits = score(pred, g)
            log_event({"type": "arm_result", "case": case["name"], "arm": arm,
                       "pred": {k: v for k, v in pred.items()
                                if k != "facts_agreement"},
                       "gold": g, "hits": hits,
                       "facts_agreement": pred.get("facts_agreement")})
            print(f"  {arm}:")
            for dim in DIMS:
                print(fmt_dim(dim, hits[dim], pred[dim]))
            if "facts_agreement" in pred:
                agree, total, missed, extra = pred["facts_agreement"]
                facts_scores.append((agree, total))
                detail = "".join(
                    [f"; missed {', '.join(missed)}" if missed else "",
                     f"; extra {', '.join(extra)}" if extra else ""])
                print(f"  [    ] facts vs oracle -> {agree}/{total}{detail}")
            rows.append((arm, hits))

    print("\n--- summary (per dimension) ---")
    for arm in arms:
        sub = [h for a, h in rows if a == arm]
        if not sub:
            continue
        parts = []
        for dim in DIMS:
            scored = [h[dim] for h in sub if h[dim] is not None]
            parts.append(f"{dim} {sum(scored)}/{len(scored)}"
                         if scored else f"{dim} -/-")
        if arm == "ground" and facts_scores:
            agree = sum(a for a, _ in facts_scores)
            total = sum(t for _, t in facts_scores)
            parts.append(f"facts {agree}/{total}")
        print(f"  {arm:<7} " + "   ".join(parts))
    if args.atoms_per_call or args.seed is not None:
        print(f"  (ground arm: atoms_per_call={args.atoms_per_call or 'all'}, "
              f"seed={args.seed})")
    return 0 if all(v for _, h in rows for v in h.values() if v is not None) else 1


if __name__ == "__main__":
    sys.exit(main())
