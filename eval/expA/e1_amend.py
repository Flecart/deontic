"""Legislative-override experiment: re-adjudicate the SAME contested cases
under amended condition definitions and measure judge recovery.

E1's error anatomy traced the adjudicator-noise tax to one epistemic-bar
atom (emergency: 24/26 wrong verdicts are emergency false-negatives). The
legislature responds the way legislatures do — by overriding the evidentiary
standard: the adjudicator's definitions switch to the `open2` redrafts
already drafted in descriptions.py (statute rules and gold semantics
unchanged). Same 57 cases in the same order, fresh store with its own
retrieval feedback, so the two stores differ only in the definitions the
judge read.

Usage:
  python e1_amend.py --judge claude-sonnet-5 --defs open2 \
      --out runs/e1/store_precedent_v2.jsonl
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "eval"))

from descriptions import GROUNDABLE                    # noqa: E402
from arms import LABELS                                # noqa: E402
from models import resolve, make_client                # noqa: E402
from precedent import Store, render_block              # noqa: E402
from adjudicator import Adjudicator                    # noqa: E402
from e1_run import defs_text, verdict_of, load_stream  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stream", default=str(HERE / "stream.jsonl"))
    ap.add_argument("--disputes", default=str(HERE / "runs/e1/disputes.jsonl"))
    ap.add_argument("--out", default=str(HERE / "runs/e1/store_precedent_v2.jsonl"))
    ap.add_argument("--judge", default="claude-sonnet-5")
    ap.add_argument("--defs", default="open2", choices=["open", "open2"])
    ap.add_argument("--burden", action="store_true",
                    help="add the standard-of-proof procedural rule")
    ap.add_argument("--seed-gold", type=int, default=0,
                    help="seed the store with N officially-decided exemplar "
                         "cases (gold findings, t=-1): the 'worked examples "
                         "shipped with the statute' institution")
    ap.add_argument("--binding", action="store_true",
                    help="strict stare decisis: precedents/exemplars bind on "
                         "like facts; distinguishing requires naming the "
                         "missing or contradicted fact")
    ap.add_argument("--seed-mandatory", action="store_true",
                    help="exemplars appear in EVERY adjudication (mandatory "
                         "authorities) instead of competing in retrieval")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--embed", default="openai", choices=["auto", "openai", "offline"])
    args = ap.parse_args()

    cases = {c["case_id"]: c for c in load_stream(args.stream)}
    contested = [json.loads(l) for l in Path(args.disputes).read_text().splitlines()
                 if l and json.loads(l)["contested"]]
    BURDEN = ("Standard of proof: decide each condition on the balance of the "
              "memo's recitals alone. Where the memo recites an uncontradicted, "
              "specific assertion by a competent party that a condition's "
              "elements are met (for example, professionals stating a present "
              "need that cannot wait), find the condition true; do not demand "
              "proof beyond the memo, and do not treat the mere possibility of "
              "alternatives as contradiction.")
    BINDING = ("Stare decisis (strict): prior adjudicated cases — and above "
               "all, officially decided examples issued with the statute — are "
               "BINDING where the memo's facts are alike on the point they "
               "decide. Follow them. You may distinguish ONLY by naming a "
               "specific fact the earlier holding required that is absent or "
               "contradicted in this memo; general doubts about a condition do "
               "not justify departing from a decided case.")
    procedure = "\n\n".join(p for p, on in ((BURDEN, args.burden),
                                            (BINDING, args.binding)) if on)
    spec = resolve(args.judge)
    judge = Adjudicator(make_client(spec), spec, LABELS, defs_text(args.defs),
                        procedure=procedure)
    store = Store(GROUNDABLE, args.embed)
    if args.seed_gold:
        # exemplars = first N SETTLED emergency-true cases (the atom the whole
        # judiciary under-finds); gold findings, no rationale needed — the
        # decided example itself carries the interpretation
        settled = {d["case_id"] for d in
                   (json.loads(l) for l in Path(args.disputes).read_text().splitlines() if l)
                   if not d["contested"]}
        picked = [c for c in cases.values()
                  if c["case_id"] in settled and c["assignment"]["emergency"]][:args.seed_gold]
        seed_holdings = [{"case_id": f"seed_{c['case_id']}", "t": -1,
                          "facts": c["narrative"],
                          "findings": {a: ("true" if v else "false")
                                       for a, v in c["assignment"].items()},
                          "verdict": c["gold"],
                          "rationale": "Officially decided example issued with the statute.",
                          "cites": [], "judge": "legislator", "contested": [],
                          "assign_key": c["assign_key"]} for c in picked]
        if not args.seed_mandatory:     # retrieval-gated: compete in the store
            for h in seed_holdings:
                store.add(h)
        print(f"seeded {len(seed_holdings)} official exemplars "
              f"({'mandatory' if args.seed_mandatory else 'retrieval-gated'})",
              file=sys.stderr)

    mand = seed_holdings if (args.seed_gold and args.seed_mandatory) else []
    ok = 0
    for d in contested:
        case = cases[d["case_id"]]
        prec = store.retrieve(case["narrative"], args.k, "embed", before_t=case["t"])
        adj = judge.adjudicate(case["narrative"], render_block(mand + prec, LABELS))
        prec = mand + prec      # recorded as seen-by-judge
        verdict = verdict_of(adj["findings"], case["acted"])
        ok += verdict["share_status"] == case["gold"]["share_status"]
        store.add({"case_id": case["case_id"], "t": case["t"],
                   "facts": case["narrative"], "findings": adj["findings"],
                   "verdict": verdict, "rationale": adj["rationale"],
                   "cites": adj["cites"], "retrieved": [p["case_id"] for p in prec],
                   "judge": args.judge, "contested": d["reasons"],
                   "assign_key": case["assign_key"]})
        print(f"t={case['t']} gold={case['gold']['share_status']:10} "
              f"judge={verdict['share_status']:10} "
              f"{'OK' if verdict['share_status'] == case['gold']['share_status'] else 'X'}",
              file=sys.stderr)
    store.save(args.out)
    print(f"defs={args.defs}: judge==gold {ok}/{len(contested)} "
          f"= {100*ok/len(contested):.1f}% (v1 open baseline: 54.4%)")
    print(f"consistency: {store.consistency()}; saved -> {args.out}")


if __name__ == "__main__":
    main()
