#!/usr/bin/env python3
"""Display a pipeline run log (runs/*.jsonl) — especially WHY facts failed.

  python docs/experiments/foia_corpus/view_run.py             # latest run
  python docs/experiments/foia_corpus/view_run.py runs/run_x.jsonl
  python docs/experiments/foia_corpus/view_run.py --failures  # only the misses,
                                                              # with the model's
                                                              # own reasoning

Each run log holds `run_meta`, one `llm_call` per API call (full prompts,
raw reply, tokens, latency) and one `arm_result` per case×arm (pred vs gold,
per-atom facts agreement). --failures joins them: for every missed/extra atom
it finds the call whose batch judged that atom and prints the reply's
reasoning, so a grounding error can be read in the model's own words.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RUNS_DIR = Path(__file__).resolve().parent / "runs"


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def reasoning_of(call: dict) -> str:
    """The 'reasoning' field of the call's JSON reply (or a reply excerpt)."""
    m = re.search(r"\{.*\}", call.get("reply", ""), re.DOTALL)
    if m:
        try:
            r = json.loads(m.group(0)).get("reasoning", "")
            return r if isinstance(r, str) else json.dumps(r, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
    return call.get("reply", "")[:400]


def calls_judging(events: list[dict], case: str, atom: str) -> list[dict]:
    """The ground-arm calls (for `case`) whose batch contained `atom`."""
    return [e for e in events
            if e.get("type") == "llm_call" and e.get("case") == case
            and e.get("arm") == "ground"
            and (atom in e.get("batch_atoms", []) or "batch_atoms" not in e)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", nargs="?", help="run file (default: latest)")
    ap.add_argument("--failures", action="store_true",
                    help="only misses, joined to the model's reasoning")
    args = ap.parse_args()

    if args.run:
        path = Path(args.run)
    else:
        candidates = sorted(RUNS_DIR.glob("run_*.jsonl"))
        if not candidates:
            print("no run logs in runs/", file=sys.stderr)
            return 1
        path = candidates[-1]
    events = load(path)
    meta = next((e for e in events if e.get("type") == "run_meta"), {})
    calls = [e for e in events if e.get("type") == "llm_call"]
    results = [e for e in events if e.get("type") == "arm_result"]
    print(f"run: {path.name}")
    print(f"  model={meta.get('model')}  arms={meta.get('arms')}  "
          f"atoms_per_call={meta.get('atoms_per_call')}  seed={meta.get('seed')}")
    print(f"  {len(calls)} llm calls, {len(results)} arm results, "
          f"{sum(c.get('prompt_tokens') or 0 for c in calls)} prompt tokens\n")

    for r in results:
        hits = r["hits"]
        missed_dims = [d for d, ok in hits.items() if ok is False]
        fa = r.get("facts_agreement")
        fact_fails = (fa[2] or fa[3]) if fa else []
        if args.failures and not missed_dims and not fact_fails:
            continue
        print(f"=== {r['case']} / {r['arm']}")
        for dim, ok in hits.items():
            mark = "---" if ok is None else ("OK " if ok else "MISS")
            print(f"  [{mark}] {dim:<12} pred={r['pred'].get(dim)}  "
                  f"gold={r['gold'].get(dim)}")
        if fa:
            agree, total, missed, extra = fa
            print(f"  facts {agree}/{total}"
                  + (f"  missed: {', '.join(missed)}" if missed else "")
                  + (f"  extra: {', '.join(extra)}" if extra else ""))
            for atom in [*missed, *extra]:
                kind = "MISSED" if atom in missed else "EXTRA"
                for c in calls_judging(events, r["case"], atom):
                    where = (f"batch {c['batch']}/{c['batches']}"
                             if "batch" in c else "single call")
                    print(f"    {kind} {atom} ({where}) — model said:")
                    print(f"      {reasoning_of(c)}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
