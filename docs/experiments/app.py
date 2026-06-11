#!/usr/bin/env python3
"""Corpus experiment run viewer API — serves */runs/*.jsonl to the React frontend.

  python docs/experiments/app.py
  cd docs/experiments/frontend && npm run dev   # http://localhost:5174
"""
from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

EXPERIMENTS_DIR = Path(__file__).resolve().parent
PORT = 8051


def discover_experiments() -> list[dict]:
    rows = []
    for path in sorted(EXPERIMENTS_DIR.iterdir()):
        if not path.is_dir() or not path.name.endswith("_corpus"):
            continue
        runs_dir = path / "runs"
        if not runs_dir.is_dir():
            continue
        run_count = len(list(runs_dir.glob("run_*.jsonl")))
        rows.append(
            {
                "id": path.name,
                "label": path.name.removesuffix("_corpus").replace("_", " ").title(),
                "run_count": run_count,
            }
        )
    return rows


def experiment_dir(exp_id: str) -> Path | None:
    path = (EXPERIMENTS_DIR / exp_id).resolve()
    base = EXPERIMENTS_DIR.resolve()
    if not path.is_dir() or path.parent != base or not exp_id.endswith("_corpus"):
        return None
    return path


def runs_dir(exp_id: str) -> Path | None:
    exp = experiment_dir(exp_id)
    if exp is None:
        return None
    rd = exp / "runs"
    return rd if rd.is_dir() else None


def load_events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


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

    dim_scores: dict[str, list[bool | None]] = {
        "disposition": [],
        "engaged": [],
        "pi": [],
    }
    facts_agree = 0
    facts_total = 0
    failure_count = 0

    cases = []
    for r in results:
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
                "hits": hits,
                "facts_agreement": fa,
                "atom_failures": atom_failures(events, r),
                "calls": [
                    c
                    for c in calls
                    if call_case_id(c) == case_id and c.get("arm") == arm
                ],
            }
        )

    def score_line(dim: str) -> str | None:
        vals = dim_scores[dim]
        scored = [v for v in vals if v is not None]
        if not scored:
            return None
        ok = sum(1 for v in scored if v)
        return f"{ok}/{len(scored)}"

    return {
        "name": path.name,
        "mtime": path.stat().st_mtime,
        "experiment": path.parent.parent.name,
        "kind": "eval",
        "meta": meta,
        "summary": {
            "llm_calls": len(calls),
            "arm_results": len(results),
            "prompt_tokens": sum(c.get("prompt_tokens") or 0 for c in calls),
            "completion_tokens": sum(c.get("completion_tokens") or 0 for c in calls),
            "seconds": round(sum(c.get("seconds") or 0 for c in calls), 2),
            "scores": {
                "disposition": score_line("disposition"),
                "engaged": score_line("engaged"),
                "pi": score_line("pi"),
                "facts": f"{facts_agree}/{facts_total}" if facts_total else None,
            },
            "failure_cases": failure_count,
        },
        "cases": cases,
    }


def summarize_run(path: Path) -> dict:
    events = load_events(path)
    meta = next((e for e in events if e.get("type") == "run_meta"), {})
    results = [e for e in events if e.get("type") == "arm_result"]
    if results:
        return summarize_eval_run(path, events, meta)
    return summarize_label_run(path, events, meta)


def list_runs(exp_id: str) -> list[dict]:
    rd = runs_dir(exp_id)
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
                "cases": meta.get("cases", []),
                "case_count": case_count,
            }
        )
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows


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

        if path == "/api/experiments":
            self._send(200, {"experiments": discover_experiments()})
            return

        if path.startswith("/api/experiments/"):
            rest = path.removeprefix("/api/experiments/")
            parts = rest.split("/", 2)

            if len(parts) == 1 and parts[0]:
                exp_id = parts[0]
                if experiment_dir(exp_id) is None:
                    self._send(404, {"error": f"experiment not found: {exp_id}"})
                    return
                self._send(200, {"runs": list_runs(exp_id)})
                return

            if len(parts) == 3 and parts[0] and parts[1] == "runs" and parts[2]:
                exp_id, run_name = parts[0], parts[2]
                rd = runs_dir(exp_id)
                if rd is None:
                    self._send(404, {"error": f"experiment not found: {exp_id}"})
                    return
                run_path = (rd / run_name).resolve()
                if not run_path.is_file() or run_path.parent != rd.resolve():
                    self._send(404, {"error": f"run not found: {run_name}"})
                    return
                self._send(200, summarize_run(run_path))
                return

        self._send(404, {"error": "not found"})


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Corpus run viewer API on http://127.0.0.1:{PORT}")
    print(f"Experiments: {', '.join(e['id'] for e in discover_experiments()) or '(none)'}")
    server.serve_forever()


if __name__ == "__main__":
    main()
