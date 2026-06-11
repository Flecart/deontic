#!/usr/bin/env python3
"""FOIA corpus run viewer API — serves runs/*.jsonl to the React frontend.

  python docs/experiments/foia_corpus/app.py          # http://localhost:8051
  cd docs/experiments/foia_corpus/frontend && npm run dev
"""
from __future__ import annotations

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

RUNS_DIR = Path(__file__).resolve().parent / "runs"
PORT = 8051


def load_events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def reasoning_of(call: dict) -> str:
    m = re.search(r"\{.*\}", call.get("reply", ""), re.DOTALL)
    if m:
        try:
            r = json.loads(m.group(0)).get("reasoning", "")
            return r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
    return (call.get("reply") or "")[:400]


def calls_judging(events: list[dict], case: str, atom: str) -> list[dict]:
    return [
        e
        for e in events
        if e.get("type") == "llm_call"
        and e.get("case") == case
        and e.get("arm") == "ground"
        and (atom in e.get("batch_atoms", []) or "batch_atoms" not in e)
    ]


def atom_failures(events: list[dict], result: dict) -> list[dict]:
    fa = result.get("facts_agreement")
    if not fa:
        return []
    missed, extra = fa[2] or [], fa[3] or []
    out: list[dict] = []
    for atom in [*missed, *extra]:
        kind = "missed" if atom in missed else "extra"
        for call in calls_judging(events, result["case"], atom):
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


def summarize_run(path: Path) -> dict:
    events = load_events(path)
    meta = next((e for e in events if e.get("type") == "run_meta"), {})
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
        cases.append(
            {
                "id": r["case"],
                "arm": r["arm"],
                "pred": r.get("pred", {}),
                "gold": r.get("gold", {}),
                "hits": hits,
                "facts_agreement": fa,
                "atom_failures": atom_failures(events, r),
                "calls": [c for c in calls if c.get("case") == r["case"] and c.get("arm") == r["arm"]],
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


def list_runs() -> list[dict]:
    rows = []
    for path in sorted(RUNS_DIR.glob("run_*.jsonl")):
        events = load_events(path)
        meta = next((e for e in events if e.get("type") == "run_meta"), {})
        results = [e for e in events if e.get("type") == "arm_result"]
        rows.append(
            {
                "name": path.name,
                "mtime": path.stat().st_mtime,
                "model": meta.get("model"),
                "arms": meta.get("arms", []),
                "cases": meta.get("cases", []),
                "case_count": len(results),
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
        if path == "/api/runs":
            self._send(200, {"runs": list_runs()})
            return
        if path.startswith("/api/runs/"):
            name = path.removeprefix("/api/runs/")
            run_path = RUNS_DIR / name
            if not run_path.is_file() or run_path.parent != RUNS_DIR.resolve():
                self._send(404, {"error": f"run not found: {name}"})
                return
            self._send(200, summarize_run(run_path))
            return
        self._send(404, {"error": "not found"})


def main() -> None:
    RUNS_DIR.mkdir(exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"FOIA run viewer API on http://127.0.0.1:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
