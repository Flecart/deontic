#!/usr/bin/env python3
"""Error anatomy: classify every wrong atom decision in the engine arms.

For each (case, atom, model, regime) where pred != gold, decide WHY using
three mechanical signals (no API calls — everything comes from the logs):

  1. the model's tri-state raw answer: "unknown" = epistemic abstention
     (the memo gives no basis, per the model) vs a confident wrong answer;
  2. cross-model consensus: if EVERY model in a regime misses the same
     (case, atom), the problem is case-level (narration/description/gold),
     not one model's misunderstanding;
  3. bank validation: if the independent annotator models also disagreed
     with gold on the exact bank instance the case used, gold itself is
     disputed.

Classes, checked in order:

  gold_disputed          consensus miss on an instance the annotators also
                         disputed -> the case/gold is not clear.
  enumeration_gap        consensus false-negative in the CLOSED regime on an
                         unlisted (tier>=1) instance -> the designed failure
                         mode of extensional definitions, not a
                         misunderstanding.
  unverifiable_intension consensus miss where every wrong model answered
                         "unknown" -> the description demands evidence the
                         memo cannot supply.
  case_unclear           consensus miss, models confidently wrong ->
                         narration/description mismatch; listed for human
                         review (use the Data QA viewer on these case ids).
  epistemic_refusal      non-consensus miss where THIS model answered
                         "unknown" -> abstention, not misreading.
  model_misread          the majority of models got it right; this model
                         misunderstood the memo or the description.

Consensus needs >=3 models in the regime; statutes with fewer (expC) only
get the per-model classes. Run from eval/:  python3 error_analysis.py
Writes error_analysis/<exp>_failures.jsonl and ERROR_ANATOMY.md.
"""
from __future__ import annotations

import ast
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPS = ["expA", "expB", "expC", "expD", "expE", "expF"]
CASE_BANKS = ["cases_stage2_memo.jsonl", "cases_memo.jsonl", "cases.jsonl"]
RESULTS = ["results_stage2_main.jsonl", "results_main.jsonl", "results.jsonl"]
ENGINE_ARMS = ("ground_open", "ground_closed")
OUT_DIR = HERE / "error_analysis"
REPORT = HERE / "ERROR_ANATOMY.md"


def pick(exp: str, names: list[str]) -> Path | None:
    for n in names:
        p = HERE / exp / n
        if p.is_file():
            return p
    return None


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.open() if l.strip()]


def groundable(exp: str) -> list[str]:
    """GROUNDABLE list from descriptions.py, parsed without executing it."""
    tree = ast.parse((HERE / exp / "descriptions.py").read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "GROUNDABLE":
                    return list(ast.literal_eval(node.value))
    raise SystemExit(f"{exp}: GROUNDABLE not found in descriptions.py")


def tri_answers(raw: str, labels: dict[str, str]) -> dict[str, str]:
    """Recover the model's true/false/unknown per atom from its raw reply."""
    if not raw:
        return {}
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        return {}
    try:
        blob = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}
    inv = {v: k for k, v in labels.items()}
    return {inv[k]: str(v).lower() for k, v in blob.items() if k in inv}


def disputed_instances(exp: str) -> set[tuple[str, str]]:
    """(atom, instance_id) pairs where any annotator disagreed with gold."""
    p = HERE / exp / "bank_validation.jsonl"
    if not p.is_file():
        return set()
    out = set()
    for r in load_jsonl(p):
        if str(r.get("annot_member")) != str(r.get("gold_member")):
            out.add((r["atom"], r["id"]))
    return out


def analyse(exp: str) -> tuple[list[dict], dict]:
    cases_p, results_p = pick(exp, CASE_BANKS), pick(exp, RESULTS)
    if not cases_p or not results_p:
        return [], {}
    atoms = groundable(exp)
    labels = {a: f"C{i+1}" for i, a in enumerate(atoms)}
    disputed = disputed_instances(exp)
    cases = {c["case_id"]: c for c in load_jsonl(cases_p)}
    rows = [r for r in load_jsonl(results_p) if r.get("arm") in ENGINE_ARMS
            and r.get("pred_assignment")]

    # pass 1: collect every miss + per-(regime, case, atom) tallies
    misses, tally = [], defaultdict(lambda: [0, 0])  # key -> [wrong, total]
    for r in rows:
        case = cases.get(r["case_id"])
        if case is None or case.get("leak_flags"):
            continue
        gold = case["assignment"]
        tri = tri_answers(r.get("raw", ""), labels)
        item_of = {it["atom"]: it.get("id") for it in case.get("items", [])}
        for a in atoms:
            key = (r["arm"], r["case_id"], a)
            tally[key][1] += 1
            if bool(r["pred_assignment"].get(a)) == bool(gold.get(a)):
                continue
            tally[key][0] += 1
            misses.append({
                "exp": exp, "case_id": r["case_id"], "atom": a,
                "model": r["model"], "regime": r["arm"],
                "tier": case.get("tier"),
                "direction": "FN" if gold.get(a) else "FP",
                "answer": tri.get(a, "?"),
                "instance": item_of.get(a),
                "gold_disputed": (a, item_of.get(a)) in disputed,
                "verdict_wrong": r.get("pred_verdict") != case.get("gold"),
            })

    # pass 2: classify
    for m in misses:
        wrong, total = tally[(m["regime"], m["case_id"], m["atom"])]
        consensus = total >= 3 and wrong == total
        peers = [x for x in misses
                 if (x["regime"], x["case_id"], x["atom"])
                 == (m["regime"], m["case_id"], m["atom"])]
        if consensus and m["gold_disputed"]:
            cls = "gold_disputed"
        elif (consensus and m["regime"] == "ground_closed"
              and m["direction"] == "FN" and (m["tier"] or 0) >= 1):
            cls = "enumeration_gap"
        elif consensus and all(p["answer"] == "unknown" for p in peers):
            cls = "unverifiable_intension"
        elif consensus:
            cls = "case_unclear"
        elif m["answer"] == "unknown":
            cls = "epistemic_refusal"
        else:
            cls = "model_misread"
        m["class"] = cls
        m["models_wrong"], m["models_total"] = wrong, total

    summary = {
        "by_class": Counter(m["class"] for m in misses),
        "by_class_regime": Counter((m["class"], m["regime"]) for m in misses),
        "misread_by_model": Counter(
            m["model"] for m in misses if m["class"] == "model_misread"),
        "refusal_by_atom": Counter(
            m["atom"] for m in misses
            if m["class"] in ("epistemic_refusal", "unverifiable_intension")),
        "unclear_cases": sorted(
            {(m["case_id"], m["atom"], m["regime"]) for m in misses
             if m["class"] in ("case_unclear", "gold_disputed")}),
        "n_rows": len(rows), "n_misses": len(misses),
    }
    return misses, summary


def snippet(exp: str, case_id: str, n: int = 220) -> str:
    cases_p = pick(exp, CASE_BANKS)
    for c in load_jsonl(cases_p):
        if c["case_id"] == case_id:
            text = " ".join(c["narrative"].split())
            return text[:n] + ("…" if len(text) > n else "")
    return ""


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    lines = ["# Error anatomy (engine arms: every error is a grounding error)",
             "", "Generated by `error_analysis.py` from the committed logs. "
             "Classes are defined in the script docstring; `case_unclear` and "
             "`gold_disputed` rows are the ones to eyeball in the Data QA "
             "viewer.", ""]
    grand = Counter()
    for exp in EXPS:
        misses, s = analyse(exp)
        if not misses:
            continue
        with (OUT_DIR / f"{exp}_failures.jsonl").open("w") as f:
            for m in misses:
                f.write(json.dumps(m) + "\n")
        grand.update(s["by_class"])
        lines += [f"## {exp} — {s['n_misses']} wrong atom decisions "
                  f"over {s['n_rows']} engine rows", ""]
        lines += ["| class | open | closed | total |", "|---|---|---|---|"]
        for cls, tot in s["by_class"].most_common():
            o = s["by_class_regime"].get((cls, "ground_open"), 0)
            c = s["by_class_regime"].get((cls, "ground_closed"), 0)
            lines.append(f"| {cls} | {o} | {c} | {tot} |")
        lines.append("")
        if s["misread_by_model"]:
            worst = ", ".join(f"{m} ({n})" for m, n
                              in s["misread_by_model"].most_common())
            lines += [f"`model_misread` by model: {worst}", ""]
        if s["refusal_by_atom"]:
            hot = ", ".join(f"`{a}` ({n})" for a, n
                            in s["refusal_by_atom"].most_common(5))
            lines += [f"Abstention concentrates on: {hot}", ""]
        unclear = s["unclear_cases"]
        if unclear:
            lines += [f"**{len(unclear)} (case, atom, regime) slots where every "
                      "model was wrong and no mechanical excuse applies** "
                      "(top 5, review in the viewer):", ""]
            for case_id, atom, regime in unclear[:5]:
                lines += [f"- `{case_id}` / `{atom}` ({regime}): "
                          f"{snippet(exp, case_id)}", ""]
    lines += ["## Pooled", "",
              "| class | total |", "|---|---|"]
    for cls, tot in grand.most_common():
        lines.append(f"| {cls} | {tot} |")
    lines.append("")
    REPORT.write_text("\n".join(lines))
    print(f"wrote {REPORT} and {OUT_DIR}/<exp>_failures.jsonl")
    for cls, tot in grand.most_common():
        print(f"  {cls:24} {tot}")


if __name__ == "__main__":
    main()
