"""E2: selection — litigation as active learning (plan_common_law.md §2 E2).

At matched store size n, which accretion policy teaches the decision boundary
best? Policies pick n precedents from the stream prefix (t < --eval-from);
grounders then classify the held-out tail with retrieval over that store.

  dispute      first n CONTESTED cases in stream order (endogenous selection;
               contested flags come from the E1 store phase's disputes.jsonl)
  uniform      n uniformly sampled prefix cases (nested across sizes)
  oracle       n cases ranked by first-pass error vs gold (# dispute models
               with a wrong verdict, then # unknown atoms) — the active-
               learning ceiling, uses gold so no live system could run it
  recency      the n prefix cases closest to the eval segment
  dispute_adj  dispute selection but with the ADJUDICATED holdings from
               store_precedent.jsonl instead of gold ones — isolates
               adjudicator noise from selection value

All policies except dispute_adj use GOLD holdings (findings = latent
assignment, no rationale): the comparison isolates *which cases* enter the
store, not who labeled them. Hypothesis: dispute ~ oracle >> uniform.

Usage:
  python e2_run.py --stream stream.jsonl --disputes runs/e1/disputes.jsonl \
      --out runs/e2/results_e2.jsonl --models gpt-4.1,deepseek-v4-flash \
      [--sizes 2,5,10,20,40] [--eval-from 140] [--store runs/e1/store_precedent.jsonl]
"""
from __future__ import annotations
import argparse, json, random, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "eval"))

from descriptions import GROUNDABLE                              # noqa: E402
from arms import LABELS                                          # noqa: E402
from models import resolve, make_client                          # noqa: E402
from precedent import Store, render_block                        # noqa: E402
from e1_run import (defs_text, ground_tri, verdict_of, load_stream,  # noqa: E402
                    gold_store_from)


# ── selection policies ────────────────────────────────────────────────────────

def select_ids(policy: str, prefix: list[dict], disputes: dict, n: int,
               rng: random.Random) -> list[str]:
    """Return case_ids of the n prefix cases the policy holds as precedent.
    Selections are nested in n (prefix of one fixed ranking per policy)."""
    if policy in ("dispute", "dispute_adj"):
        ranked = [c for c in prefix if disputes[c["case_id"]]["contested"]]
    elif policy == "uniform":
        ranked = prefix[:]
        rng.shuffle(ranked)
    elif policy == "oracle":
        def err(c):
            d = disputes[c["case_id"]]
            wrong = sum(v != d["gold"] for v in d["first_verdicts"].values())
            unk = sum(list(t.values()).count("unknown")
                      for t in d["first_pass"].values())
            return (-wrong, -unk, c["t"])
        ranked = sorted(prefix, key=err)
    elif policy == "recency":
        ranked = sorted(prefix, key=lambda c: -c["t"])
    else:
        raise ValueError(policy)
    return [c["case_id"] for c in ranked[:n]]


def substore(full: Store, ids: list[str], embed_provider: str) -> Store:
    st = Store(GROUNDABLE, embed_provider)
    by_id = {h["case_id"]: h for h in full.holdings}
    st.holdings = [by_id[i] for i in ids if i in by_id]
    return st


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stream", default=str(HERE / "stream.jsonl"))
    ap.add_argument("--disputes", default=str(HERE / "runs/e1/disputes.jsonl"))
    ap.add_argument("--store", default=str(HERE / "runs/e1/store_precedent.jsonl"),
                    help="adjudicated store (for dispute_adj); optional")
    ap.add_argument("--out", default=str(HERE / "runs/e2/results_e2.jsonl"))
    ap.add_argument("--policies", default="dispute,uniform,oracle,recency,dispute_adj")
    ap.add_argument("--sizes", default="2,5,10,20,40")
    ap.add_argument("--eval-from", type=int, default=140,
                    help="eval segment = cases with t >= this; store pool = t < this")
    ap.add_argument("--models", default="stub")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--embed", default="auto", choices=["auto", "openai", "offline"])
    args = ap.parse_args()

    cases = load_stream(args.stream)
    prefix = [c for c in cases if c["t"] < args.eval_from]
    tail = [c for c in cases if c["t"] >= args.eval_from]
    disputes = {json.loads(l)["case_id"]: json.loads(l)
                for l in Path(args.disputes).read_text().splitlines() if l}
    gold_full = gold_store_from(prefix, args.embed)
    adj_full = None
    policies = args.policies.split(",")
    if "dispute_adj" in policies:
        if Path(args.store).exists():
            adj_full = Store.load(args.store, GROUNDABLE, args.embed)
        else:
            policies.remove("dispute_adj")
            print("no adjudicated store found; skipping dispute_adj", file=sys.stderr)
    sizes = [int(s) for s in args.sizes.split(",")]
    open_defs = defs_text("open")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out = open(args.out, "w")
    n_rows = 0
    for policy in policies:
        for n in sizes:
            # fresh same-seed rng per call -> identical shuffle -> nested S_n
            ids = select_ids(policy, prefix, disputes, n, random.Random(args.seed))
            full = adj_full if policy == "dispute_adj" else gold_full
            st = substore(full, ids, args.embed)
            if len(st) < n:
                print(f"{policy} n={n}: only {len(st)} available", file=sys.stderr)
            for mname in args.models.split(","):
                spec = resolve(mname)
                client = make_client(spec)

                def one(case, st=st, spec=spec, client=client, policy=policy,
                        n=n, mname=mname):
                    t0 = time.time()
                    try:
                        prec = st.retrieve(case["narrative"], args.k, "embed")
                        block = render_block(prec, LABELS,
                                             show_rationale=(policy == "dispute_adj"))
                        tri, toks, raw = ground_tri(client, spec, case["narrative"],
                                                    open_defs, prec_block=block)
                        res = {"pred_tri": tri,
                               "pred_verdict": verdict_of(tri, case["acted"]),
                               "retrieved": [h["case_id"] for h in prec],
                               "n_relevant_retrieved": sum(
                                   1 for h in prec
                                   if h["assign_key"] == case["assign_key"]),
                               "n_relevant_available": sum(
                                   1 for h in st.holdings
                                   if h["assign_key"] == case["assign_key"]),
                               "tokens": toks, "secs": round(time.time() - t0, 2),
                               "raw": raw}
                    except Exception as e:
                        res = {"pred_tri": None,
                               "pred_verdict": {"share_status": f"ERROR:{type(e).__name__}",
                                                "violation": False,
                                                "notify_required": False},
                               "retrieved": [], "n_relevant_retrieved": 0,
                               "n_relevant_available": 0, "tokens": 0, "secs": 0,
                               "raw": str(e)[:300]}
                    return {"case_id": case["case_id"], "t": case["t"],
                            "tier": case["tier"], "acted": case["acted"],
                            "assign_key": case["assign_key"], "policy": policy,
                            "store_n": len(st), "model": mname,
                            "gold": case["gold"],
                            "gold_assignment": case["assignment"], **res}

                with ThreadPoolExecutor(max_workers=args.workers) as pool:
                    for row in pool.map(one, tail):
                        out.write(json.dumps(row) + "\n")
                        out.flush()
                        n_rows += 1
                print(f"done policy={policy} n={n} model={mname}", file=sys.stderr)
    out.close()
    print(f"wrote {n_rows} rows -> {args.out} "
          f"({len(tail)} eval cases x {len(policies)} policies x {len(sizes)} sizes)")


if __name__ == "__main__":
    main()
