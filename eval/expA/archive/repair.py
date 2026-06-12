"""Repair experiment: precedent accretion for the closed regime.

The institutional claim under test: when an open-textured instance defeats a
closed enumeration (Tier-2 miss), the system is repaired *locally* — append the
decided instance to the enumeration (a precedent: "as held, a gait-signature
profile counts") — and the fix (a) generalizes to other cases of the same
instance type, (b) does not regress in-distribution behavior.

Protocol:
  1. find ground_closed Tier-2 rows (model M) with missed true atoms;
  2. take the missed (atom, item) pairs from HELD-OUT repair cases (first
     --holdout fraction of distinct case ids) — precedents come only from
     those; evaluation is on the remaining Tier-2 cases + all Tier-0/1 cases;
  3. re-ground eval cases with the repaired closed descriptions;
  4. report Tier-2 fix rate (on unseen cases of precedented types vs
     unprecedented types) and Tier-0/1 regression.

Usage:
  python repair.py --cases cases_stage1c.jsonl --results results_stage1c.jsonl \
      --model gpt-4.1 [--holdout 0.5] [--out repair_results.jsonl]
"""
from __future__ import annotations
import argparse, json, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))

from descriptions import ATOMS, GROUNDABLE                     # noqa: E402
from arms import GROUND_PROMPT, LABELS, parse_json_blob        # noqa: E402
from gen_cases import engine_verdict                           # noqa: E402
from models import resolve, make_client                        # noqa: E402
from agents import _create                                     # noqa: E402
from concurrent.futures import ThreadPoolExecutor              # noqa: E402


def ground(client, spec, memo, defs_by_atom):
    defs = "\n".join(f"- {LABELS[a]}: {defs_by_atom[a]}" for a in GROUNDABLE)
    r = _create(client, spec, [{"role": "user",
                                "content": GROUND_PROMPT.format(defs=defs, memo=memo)}])
    blob = parse_json_blob(r.choices[0].message.content or "") or {}
    inv = {v: k for k, v in LABELS.items()}
    return {atom: str(blob.get(lbl, "unknown")).lower() == "true"
            for lbl, atom in inv.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=str(HERE / "cases_stage1c.jsonl"))
    ap.add_argument("--results", default=str(HERE / "results_stage1c.jsonl"))
    ap.add_argument("--model", default="gpt-4.1")
    ap.add_argument("--holdout", type=float, default=0.5)
    ap.add_argument("--out", default=str(HERE / "repair_results.jsonl"))
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    cases = {json.loads(l)["case_id"]: json.loads(l)
             for l in Path(args.cases).read_text().splitlines() if l}
    rows = [json.loads(l) for l in Path(args.results).read_text().splitlines() if l]
    closed_rows = [r for r in rows if r["arm"] == "ground_closed"
                   and r["model"] == args.model and r["tier"] == 2
                   and r["pred_assignment"]]

    # precedent source = first holdout fraction of distinct tier-2 cases
    ids = sorted({r["case_id"] for r in closed_rows})
    cut = max(1, int(len(ids) * args.holdout))
    precedent_ids, eval_t2_ids = set(ids[:cut]), set(ids[cut:])

    # collect missed true atoms in precedent cases -> their items become holdings
    holdings = defaultdict(set)        # atom -> {item phrases}
    precedented_types = defaultdict(set)  # atom -> {item ids}
    for r in closed_rows:
        if r["case_id"] not in precedent_ids:
            continue
        case = cases[r["case_id"]]
        for it in case["items"]:
            if it["polarity"] and not r["pred_assignment"][it["atom"]]:
                holdings[it["atom"]].add(it["phrase"])
                precedented_types[it["atom"]].add(it["id"])

    repaired = {}
    for a in GROUNDABLE:
        d = ATOMS[a]["closed"]
        if holdings[a]:
            d += "; or, as held in prior decisions: " + "; ".join(sorted(holdings[a]))
        repaired[a] = d
    print(f"precedents from {len(precedent_ids)} cases: "
          f"{ {a: len(v) for a, v in holdings.items() if v} }")

    spec = resolve(args.model)
    client = make_client(spec)
    eval_rows = [r for r in rows if r["arm"] == "ground_closed" and r["model"] == args.model
                 and (r["case_id"] in eval_t2_ids or r["tier"] in (0, 1))]

    def one(r):
        case = cases[r["case_id"]]
        assign = ground(client, spec, case["narrative"], repaired)
        verdict = engine_verdict([a for a, t in assign.items() if t], case["acted"])
        return {"case_id": r["case_id"], "tier": r["tier"],
                "before_ok": r["pred_verdict"]["share_status"] == r["gold"]["share_status"],
                "after_ok": verdict["share_status"] == r["gold"]["share_status"],
                "gold": r["gold"], "after_verdict": verdict, "after_assignment": assign,
                "precedented": any(it["polarity"] and it["id"] in precedented_types[it["atom"]]
                                   for it in case["items"])}

    out_rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        out_rows = list(pool.map(one, eval_rows))
    Path(args.out).write_text("\n".join(json.dumps(r) for r in out_rows) + "\n")

    def acc(rs, key):
        sel = [r[key] for r in rs]
        return f"{100*sum(sel)/len(sel):5.1f}% ({sum(sel)}/{len(sel)})" if sel else "-"
    t2 = [r for r in out_rows if r["tier"] == 2]
    t2p = [r for r in t2 if r["precedented"]]
    t2u = [r for r in t2 if not r["precedented"]]
    t01 = [r for r in out_rows if r["tier"] in (0, 1)]
    print(f"tier-2 eval (unseen cases):  before {acc(t2,'before_ok')}  after {acc(t2,'after_ok')}")
    print(f"  with precedented type:     before {acc(t2p,'before_ok')}  after {acc(t2p,'after_ok')}")
    print(f"  without precedented type:  before {acc(t2u,'before_ok')}  after {acc(t2u,'after_ok')}")
    print(f"tier-0/1 regression check:   before {acc(t01,'before_ok')}  after {acc(t01,'after_ok')}")


if __name__ == "__main__":
    main()
