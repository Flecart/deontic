#!/usr/bin/env python3
"""Eval run viewer API — corpus experiments + modal ToM results.

  python docs/experiments/app.py
  cd docs/experiments/frontend && npm install && npm run dev
"""
from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[2]
EXPERIMENT_ROOTS = [
    REPO / "docs" / "experiments",
    REPO / "archive" / "experiments",
]
MODAL_RESULTS = REPO.parent / "modal" / "results"
EXPA_ROOT = REPO / "eval" / "expA"
PORT = 8051


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def load_events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


# ── corpus experiments ───────────────────────────────────────────────────────


def discover_corpus_experiments() -> list[dict]:
    seen: set[str] = set()
    rows: list[dict] = []
    for root in EXPERIMENT_ROOTS:
        if not root.is_dir():
            continue
        for path in sorted(root.iterdir()):
            if not path.is_dir() or not path.name.endswith("_corpus"):
                continue
            if path.name in seen:
                continue
            runs_dir = path / "runs"
            if not runs_dir.is_dir():
                continue
            seen.add(path.name)
            rows.append(
                {
                    "id": path.name,
                    "label": path.name.removesuffix("_corpus").replace("_", " ").title(),
                    "type": "corpus",
                    "run_count": len(list(runs_dir.glob("run_*.jsonl"))),
                }
            )
    return rows


def corpus_dir(exp_id: str) -> Path | None:
    for root in EXPERIMENT_ROOTS:
        path = (root / exp_id).resolve()
        if path.is_dir() and path.name == exp_id and path.parent.resolve() == root.resolve():
            return path
    return None


def corpus_runs_dir(exp_id: str) -> Path | None:
    exp = corpus_dir(exp_id)
    if exp is None:
        return None
    rd = exp / "runs"
    return rd if rd.is_dir() else None


def parse_reply_json(reply: str) -> dict:
    m = re.search(r"\{.*\}", reply or "", re.DOTALL)
    if not m:
        return {}
    try:
        parsed = json.loads(m.group(0))
        return parsed if isinstance(parsed, dict) else {}
    except json.JSONDecodeError:
        return {}


def reasoning_of(call: dict) -> str:
    parsed = parse_reply_json(call.get("reply", ""))
    for key in ("reasoning", "notes"):
        val = parsed.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return (call.get("reply") or "")[:400]


def call_case_id(call: dict) -> str:
    return str(call.get("case") or call.get("slug") or "?")


def calls_judging(events: list[dict], case: str, arm: str, atom: str) -> list[dict]:
    return [
        e
        for e in events
        if e.get("type") == "llm_call"
        and call_case_id(e) == case
        and e.get("arm") == arm
        and (atom in e.get("batch_atoms", []) or "batch_atoms" not in e)
    ]


def atom_failures(events: list[dict], result: dict) -> list[dict]:
    fa = result.get("facts_agreement")
    if not fa:
        return []
    missed, extra = fa[2] or [], fa[3] or []
    arm = result.get("arm", "ground")
    out: list[dict] = []
    for atom in [*missed, *extra]:
        kind = "missed" if atom in missed else "extra"
        for call in calls_judging(events, result["case"], arm, atom):
            where = (
                f"batch {call['batch']}/{call['batches']}"
                if "batch" in call
                else "single call"
            )
            out.append(
                {
                    "atom": atom,
                    "kind": kind,
                    "where": where,
                    "reasoning": reasoning_of(call),
                    "call_ts": call.get("ts"),
                }
            )
    return out


def _arm_order(meta: dict, arms_seen: set[str]) -> list[str]:
    preferred = ["oracle", "ground", "llm"]
    from_meta = [a for a in meta.get("arms", []) if a in arms_seen]
    rest = sorted(arms_seen - set(from_meta) - set(preferred))
    ordered = [a for a in preferred if a in arms_seen]
    for a in from_meta:
        if a not in ordered:
            ordered.append(a)
    ordered.extend(rest)
    return ordered


def _score_line(vals: list[bool | None]) -> str | None:
    scored = [v for v in vals if v is not None]
    if not scored:
        return None
    ok = sum(1 for v in scored if v)
    return f"{ok}/{len(scored)}"


def _summarize_arm_results(arm_results: list[dict]) -> dict:
    dim_scores: dict[str, list[bool | None]] = {
        "disposition": [],
        "engaged": [],
        "pi": [],
    }
    facts_agree = 0
    facts_total = 0
    failure_count = 0
    for r in arm_results:
        hits = r.get("hits", {})
        for dim in dim_scores:
            dim_scores[dim].append(hits.get(dim))
        fa = r.get("facts_agreement")
        if fa:
            facts_agree += fa[0]
            facts_total += fa[1]
        missed_dims = [d for d, ok in hits.items() if ok is False]
        fact_fails = bool(fa and (fa[2] or fa[3])) if fa else False
        if missed_dims or fact_fails:
            failure_count += 1
    return {
        "cases": len(arm_results),
        "scores": {
            "disposition": _score_line(dim_scores["disposition"]),
            "engaged": _score_line(dim_scores["engaged"]),
            "pi": _score_line(dim_scores["pi"]),
            "facts": f"{facts_agree}/{facts_total}" if facts_total else None,
        },
        "failure_cases": failure_count,
    }


def summarize_label_run(path: Path, events: list[dict], meta: dict) -> dict:
    calls = [e for e in events if e.get("type") == "llm_call"]
    cases = []
    for call in calls:
        label = parse_reply_json(call.get("reply", ""))
        cases.append(
            {
                "id": call_case_id(call),
                "arm": call.get("arm", "label"),
                "kind": "label",
                "label": label,
                "pred": {},
                "gold": {},
                "hits": {},
                "facts_agreement": None,
                "atom_failures": [],
                "calls": [call],
            }
        )
    return {
        "name": path.name,
        "mtime": path.stat().st_mtime,
        "source": "corpus",
        "experiment": path.parent.parent.name,
        "kind": "label",
        "meta": meta,
        "summary": {
            "llm_calls": len(calls),
            "arm_results": 0,
            "prompt_tokens": sum(c.get("prompt_tokens") or 0 for c in calls),
            "completion_tokens": sum(c.get("completion_tokens") or 0 for c in calls),
            "seconds": round(sum(c.get("seconds") or 0 for c in calls), 2),
            "scores": {
                "disposition": None,
                "engaged": None,
                "pi": None,
                "facts": None,
            },
            "failure_cases": 0,
        },
        "cases": cases,
    }


def summarize_eval_run(path: Path, events: list[dict], meta: dict) -> dict:
    calls = [e for e in events if e.get("type") == "llm_call"]
    results = [e for e in events if e.get("type") == "arm_result"]

    by_arm_raw: dict[str, list[dict]] = {}
    for r in results:
        by_arm_raw.setdefault(r["arm"], []).append(r)

    arms_seen = set(by_arm_raw)
    by_arm = {
        arm: _summarize_arm_results(by_arm_raw[arm])
        for arm in _arm_order(meta, arms_seen)
    }
    overall = _summarize_arm_results(results)

    cases = []
    for r in results:
        case_id = r["case"]
        arm = r["arm"]
        cases.append(
            {
                "id": case_id,
                "arm": arm,
                "kind": "eval",
                "label": None,
                "pred": r.get("pred", {}),
                "gold": r.get("gold", {}),
                "hits": r.get("hits", {}),
                "facts_agreement": r.get("facts_agreement"),
                "atom_failures": atom_failures(events, r),
                "calls": [
                    c
                    for c in calls
                    if call_case_id(c) == case_id and c.get("arm") == arm
                ],
            }
        )

    return {
        "name": path.name,
        "mtime": path.stat().st_mtime,
        "source": "corpus",
        "experiment": path.parent.parent.name,
        "kind": "eval",
        "meta": meta,
        "summary": {
            "llm_calls": len(calls),
            "arm_results": len(results),
            "prompt_tokens": sum(c.get("prompt_tokens") or 0 for c in calls),
            "completion_tokens": sum(c.get("completion_tokens") or 0 for c in calls),
            "seconds": round(sum(c.get("seconds") or 0 for c in calls), 2),
            "scores": overall["scores"],
            "failure_cases": overall["failure_cases"],
            "by_arm": by_arm,
        },
        "cases": cases,
    }


def summarize_corpus_run(path: Path) -> dict:
    events = load_events(path)
    meta = next((e for e in events if e.get("type") == "run_meta"), {})
    results = [e for e in events if e.get("type") == "arm_result"]
    if results:
        return summarize_eval_run(path, events, meta)
    return summarize_label_run(path, events, meta)


def list_corpus_runs(exp_id: str) -> list[dict]:
    rd = corpus_runs_dir(exp_id)
    if rd is None:
        return []
    rows = []
    for path in sorted(rd.glob("run_*.jsonl")):
        events = load_events(path)
        meta = next((e for e in events if e.get("type") == "run_meta"), {})
        results = [e for e in events if e.get("type") == "arm_result"]
        label_calls = [e for e in events if e.get("type") == "llm_call" and e.get("arm") == "label"]
        if results:
            kind = "eval"
            arms = meta.get("arms", [])
            case_count = len(results)
            model = meta.get("model")
        elif label_calls:
            kind = "label"
            arms = ["label"]
            case_count = len(label_calls)
            model = label_calls[0].get("model")
        else:
            kind = "other"
            arms = meta.get("arms", [])
            case_count = len(results)
            model = meta.get("model")
        rows.append(
            {
                "name": path.name,
                "mtime": path.stat().st_mtime,
                "kind": kind,
                "model": model,
                "arms": arms,
                "case_count": case_count,
            }
        )
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows


# ── Experiment A case banks ───────────────────────────────────────────────────


def expa_available() -> bool:
    return EXPA_ROOT.is_dir()


def assignment_prefix(case_id: str) -> str:
    parts = case_id.split("_")
    return parts[0] if parts else case_id


def list_expa_banks() -> list[dict]:
    if not expa_available():
        return []
    rows = []
    for path in sorted(EXPA_ROOT.glob("cases_*.jsonl")):
        cases = load_events(path)
        rows.append(
            {
                "name": path.name,
                "mtime": path.stat().st_mtime,
                "kind": "casebank",
                "case_count": len(cases),
            }
        )
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows


def summarize_casebank(path: Path) -> dict:
    cases = load_events(path)
    by_tier: dict[int, int] = {}
    by_share: dict[str, int] = {}
    acted = 0
    leaky = 0
    assignments: set[str] = set()
    for c in cases:
        by_tier[c.get("tier", -1)] = by_tier.get(c.get("tier", -1), 0) + 1
        share = (c.get("gold") or {}).get("share_status", "?")
        by_share[share] = by_share.get(share, 0) + 1
        if c.get("acted"):
            acted += 1
        if c.get("leak_flags"):
            leaky += 1
        assignments.add(assignment_prefix(c.get("case_id", "")))
    return {
        "name": path.name,
        "mtime": path.stat().st_mtime,
        "source": "casebank",
        "experiment": "expA",
        "kind": "casebank",
        "meta": {"path": str(path.relative_to(REPO))},
        "summary": {
            "case_count": len(cases),
            "acted_count": acted,
            "pending_count": len(cases) - acted,
            "leaky_count": leaky,
            "assignment_count": len(assignments),
            "by_tier": {str(k): v for k, v in sorted(by_tier.items())},
            "by_share_status": by_share,
        },
        "cases": cases,
    }


# ── modal ToM ────────────────────────────────────────────────────────────────


def modal_available() -> bool:
    return MODAL_RESULTS.is_dir()


def question_type(q: str) -> str:
    q = q.lower()
    if "think that" in q or "searches for" in q:
        return "second_order"
    if "think" in q or "look for" in q or "will" in q:
        return "first_order"
    if "beginning" in q or "was the" in q:
        return "memory"
    return "factual"


def list_modal_runs() -> list[dict]:
    if not modal_available():
        return []
    rows = []
    for path in sorted(MODAL_RESULTS.iterdir()):
        if not path.is_dir():
            continue
        summary_path = path / "summary.json"
        if not summary_path.is_file():
            continue
        summary = load_json(summary_path)
        run = summary.get("run", {})
        n = run.get("n_problems") or summary.get("overall", {}).get("cot", {}).get("total", 0)
        rows.append(
            {
                "name": path.name,
                "mtime": path.stat().st_mtime,
                "kind": "modal",
                "model": run.get("model"),
                "arms": ["cot", "kb"],
                "case_count": n,
            }
        )
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows


def _modal_arm_row(arm: str, correct: int, total: int, failures: int, extra: dict | None = None) -> dict:
    row = {
        "cases": total,
        "scores": {
            "accuracy": f"{correct}/{total}" if total else None,
            "disposition": None,
            "engaged": None,
            "pi": None,
            "facts": None,
        },
        "failure_cases": failures,
    }
    if extra:
        row["scores"].update(extra)
    return row


def summarize_modal_run(path: Path) -> dict:
    summary = load_json(path / "summary.json")
    details_path = path / "details.jsonl"
    records = load_events(details_path) if details_path.is_file() else []

    run_meta = summary.get("run", {})
    overall = summary.get("overall", {})
    by_qt = summary.get("by_question_type", {})

    cot_correct = sum(1 for r in records if r.get("cot", {}).get("correct"))
    kb_correct = sum(1 for r in records if r.get("kb", {}).get("correct"))
    kb_parsed = sum(1 for r in records if r.get("kb", {}).get("parse_error") is None)
    n = len(records) or run_meta.get("n_problems", 0)

    cases: list[dict] = []
    for rec in records:
        pid = str(rec.get("problem_id", "?"))
        story = rec.get("story", [])
        qtype = question_type(rec.get("cot", {}).get("question", ""))
        for arm in ("cot", "kb"):
            arm_data = rec.get(arm, {})
            calls = []
            if arm == "cot":
                calls = [
                    {
                        "ts": "",
                        "type": "llm_call",
                        "arm": "cot",
                        "reply": arm_data.get("raw", ""),
                        "seconds": arm_data.get("latency_s"),
                        "prompt_tokens": (arm_data.get("usage") or {}).get("prompt_tokens"),
                        "completion_tokens": (arm_data.get("usage") or {}).get("completion_tokens"),
                        "user": "Story:\n" + "\n".join(story) + "\n\nQuestion: " + arm_data.get("question", ""),
                    }
                ]
            else:
                calls = [
                    {
                        "ts": "",
                        "type": "llm_call",
                        "arm": "kb",
                        "reply": arm_data.get("raw_answer", ""),
                        "system": arm_data.get("raw_formalize", ""),
                        "user": arm_data.get("kml", ""),
                        "seconds": arm_data.get("latency_s"),
                        "proof_trace": arm_data.get("proof_trace"),
                        "parse_error": arm_data.get("parse_error"),
                    }
                ]
            cases.append(
                {
                    "id": pid,
                    "arm": arm,
                    "kind": "modal",
                    "question_type": qtype,
                    "story": story,
                    "question": arm_data.get("question"),
                    "expected": arm_data.get("expected"),
                    "predicted": arm_data.get("predicted"),
                    "correct": arm_data.get("correct"),
                    "parse_error": arm_data.get("parse_error") if arm == "kb" else None,
                    "pred": {"answer": arm_data.get("predicted")},
                    "gold": {"answer": arm_data.get("expected")},
                    "hits": {"correct": arm_data.get("correct")},
                    "facts_agreement": None,
                    "atom_failures": [],
                    "calls": calls,
                }
            )

    cot_total = overall.get("cot", {}).get("total", n)
    kb_total = overall.get("kb", {}).get("total", n)
    cot_ok = overall.get("cot", {}).get("correct", cot_correct)
    kb_ok = overall.get("kb", {}).get("correct", kb_correct)

    return {
        "name": path.name,
        "mtime": path.stat().st_mtime,
        "source": "modal",
        "experiment": "modal",
        "kind": "modal",
        "meta": run_meta,
        "summary": {
            "llm_calls": n * 2,
            "arm_results": n * 2,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "seconds": run_meta.get("elapsed_s", 0),
            "scores": {
                "cot": f"{cot_ok}/{cot_total}" if cot_total else None,
                "kb": f"{kb_ok}/{kb_total}" if kb_total else None,
                "disposition": None,
                "engaged": None,
                "pi": None,
                "facts": None,
            },
            "failure_cases": (cot_total - cot_ok) + (kb_total - kb_ok),
            "by_arm": {
                "cot": _modal_arm_row("cot", cot_ok, cot_total, cot_total - cot_ok),
                "kb": _modal_arm_row(
                    "kb",
                    kb_ok,
                    kb_total,
                    kb_total - kb_ok,
                    {"parse": f"{kb_parsed}/{n}" if n else None},
                ),
            },
            "by_question_type": by_qt,
            "kb_parse_success": summary.get("kb_parse_success"),
        },
        "cases": cases,
    }


# ── HTTP ─────────────────────────────────────────────────────────────────────


def discover_sources() -> list[dict]:
    sources = discover_corpus_experiments()
    if expa_available() and list_expa_banks():
        sources.insert(
            0,
            {
                "id": "expA",
                "label": "Experiment A",
                "type": "casebank",
                "run_count": len(list_expa_banks()),
            },
        )
    if modal_available() and list_modal_runs():
        sources.insert(
            0,
            {
                "id": "modal",
                "label": "Modal ToM",
                "type": "modal",
                "run_count": len(list_modal_runs()),
            },
        )
    return sources


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def _send(self, status: int, body: dict | list) -> None:
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        path = unquote(self.path.split("?", 1)[0])

        if path == "/api/sources":
            self._send(200, {"sources": discover_sources()})
            return

        if path.startswith("/api/sources/"):
            rest = path.removeprefix("/api/sources/")
            parts = rest.split("/")

            if len(parts) == 2 and parts[1] == "runs" and parts[0]:
                source_id = parts[0]
                if source_id == "expA":
                    self._send(200, {"runs": list_expa_banks()})
                    return
                if source_id == "modal":
                    self._send(200, {"runs": list_modal_runs()})
                    return
                if corpus_dir(source_id):
                    self._send(200, {"runs": list_corpus_runs(source_id)})
                    return
                self._send(404, {"error": f"source not found: {source_id}"})
                return

            if len(parts) == 3 and parts[1] == "runs" and parts[0] and parts[2]:
                source_id, run_name = parts[0], parts[2]
                if source_id == "expA":
                    bank_path = (EXPA_ROOT / run_name).resolve()
                    if (
                        not bank_path.is_file()
                        or bank_path.parent != EXPA_ROOT.resolve()
                        or not bank_path.name.startswith("cases_")
                    ):
                        self._send(404, {"error": f"case bank not found: {run_name}"})
                        return
                    self._send(200, summarize_casebank(bank_path))
                    return
                if source_id == "modal":
                    run_path = (MODAL_RESULTS / run_name).resolve()
                    if not run_path.is_dir() or run_path.parent != MODAL_RESULTS.resolve():
                        self._send(404, {"error": f"run not found: {run_name}"})
                        return
                    self._send(200, summarize_modal_run(run_path))
                    return
                rd = corpus_runs_dir(source_id)
                if rd is None:
                    self._send(404, {"error": f"source not found: {source_id}"})
                    return
                run_path = (rd / run_name).resolve()
                if not run_path.is_file() or run_path.parent != rd.resolve():
                    self._send(404, {"error": f"run not found: {run_name}"})
                    return
                self._send(200, summarize_corpus_run(run_path))
                return

        self._send(404, {"error": "not found"})


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Eval run viewer API on http://127.0.0.1:{PORT}")
    for s in discover_sources():
        print(f"  {s['type']:6} {s['id']} ({s['run_count']} runs)")
    server.serve_forever()


if __name__ == "__main__":
    main()
