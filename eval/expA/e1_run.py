"""E1 pipeline on expA (plan_common_law.md §2 E1; M0 wiring).

Two phases so the store is built once and every panel model then reads the
SAME body of precedent (shared law -> inter-model agreement is meaningful,
and eval stays embarrassingly parallel):

  store   Stream the cases in order. Two cheap first-pass grounders classify
          each case precedent-free; a case is CONTESTED when their engine
          verdicts disagree, either reports an unknown atom, or the engine
          returns the unresolved ([JUDGE]) class. Contested cases go to the
          adjudicator (default claude-sonnet-5) with top-k retrieval over the
          store so far; its holding accretes. A matched-size uniform store
          (same judge, uniformly chosen cases, same accretion clock) is built
          alongside — the E1 selection ablation's control.

  eval    Every (arm x model) classifies every case against the frozen
          stores with as-of-t retrieval (only holdings with t' < t).
          Arms: oracle, program, ground_closed, ground_open, ground_hybrid
          (static frontier), precedent[@embed|@atom|@rule] (ours),
          uniform (RAG ablation), goldfs (gold few-shot ceiling).

Verdicts are ALWAYS the engine's on the grounded atoms; no model emits a
verdict. Usage:

  python e1_run.py store --stream stream.jsonl --out-dir runs/e1 \
      --dispute-models gpt-4.1,deepseek-v4-flash --judge claude-sonnet-5
  python e1_run.py eval  --stream stream.jsonl --out-dir runs/e1 \
      --models cheap_panel --arms oracle,program,ground_closed,ground_open,ground_hybrid,precedent@embed,uniform,goldfs
"""
from __future__ import annotations
import argparse, json, random, sys, time
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "eval"))

from descriptions import ATOMS, GROUNDABLE                      # noqa: E402
from arms import GROUND_PROMPT, LABELS, parse_json_blob          # noqa: E402
import gen_cases                                                 # noqa: E402
from models import resolve, make_client, CHEAP_PANEL, FULL_PANEL  # noqa: E402
from agents import _create                                       # noqa: E402
from precedent import Store, render_block                        # noqa: E402
from adjudicator import Adjudicator                              # noqa: E402

CLOSED_IDS = {a: {iid for iid, _ in ATOMS[a]["closed_items"]} for a in GROUNDABLE}


# ── engine verdicts (cached: same assignment recurs across the stream) ────────

@lru_cache(maxsize=None)
def _verdict(trues: tuple, acted: bool) -> tuple:
    return tuple(sorted(gen_cases.engine_verdict(list(trues), acted).items()))


def verdict_of(tri: dict, acted: bool) -> dict:
    trues = tuple(sorted(a for a, v in tri.items() if v == "true"))
    return dict(_verdict(trues, acted))


# ── condition definitions per drafting regime ─────────────────────────────────

def _def_of(atom: str, regime: str) -> str:
    if regime == "hybrid":
        return (ATOMS[atom]["closed"]
                + "; or, beyond the listed categories, any case where "
                + ATOMS[atom]["open"])
    if regime == "open2":   # evidentiary redrafts where drafted; open elsewhere
        return ATOMS[atom].get("open2", ATOMS[atom]["open"])
    return ATOMS[atom][regime]


def defs_text(regime: str) -> str:
    return "\n".join(f"- {LABELS[a]}: {_def_of(a, regime)}" for a in GROUNDABLE)


# ── grounding calls ───────────────────────────────────────────────────────────

PREC_GROUND_PROMPT = """You are a careful fact classifier for an automated \
compliance pipeline. Below are condition definitions, prior adjudicated cases \
(an adjudicator's findings on earlier memos under the SAME conditions), and a \
memo describing a dataset hand-off between two automated agents. For EACH \
condition, decide from the memo whether it holds: true, false, or unknown \
(unknown = the memo gives no sufficient basis either way).

The prior cases are precedent: where the memo's facts are alike on the point a \
prior case decides, follow it; where they differ in a way that matters, you may \
distinguish it. Precedents guide borderline judgment; the definitions govern.

Conditions:
{defs}

Prior adjudicated cases:
{precedents}

Memo:
{memo}

Reply with ONLY a JSON object mapping each condition name to "true", "false" or \
"unknown". Example: {{"C1": "true", "C2": "false"}}"""


GROUND_TIMEOUT = 180        # s per grounding call; a hung provider must not stall the stream


def ground_tri(client, spec, memo: str, defs: str, prec_block: str | None = None):
    """One batched grounding call; tri-state result. Returns (tri, toks, raw)."""
    if prec_block is None:
        prompt = GROUND_PROMPT.format(defs=defs, memo=memo)
    else:
        prompt = PREC_GROUND_PROMPT.format(defs=defs, precedents=prec_block, memo=memo)
    if hasattr(client, "with_options"):       # StubClient has no options
        client = client.with_options(timeout=GROUND_TIMEOUT, max_retries=1)
    r = _create(client, spec, [{"role": "user", "content": prompt}])
    text = r.choices[0].message.content or ""
    blob = parse_json_blob(text) or {}
    tri = {}
    for a in GROUNDABLE:
        v = str(blob.get(LABELS[a], "unknown")).lower()
        tri[a] = v if v in ("true", "false") else "unknown"
    usage = getattr(r, "usage", None)
    toks = (usage.prompt_tokens + usage.completion_tokens) if usage else 0
    return tri, toks, text


def load_stream(path: str) -> list[dict]:
    cases = [json.loads(l) for l in Path(path).read_text().splitlines() if l]
    assert all(c["t"] == i for i, c in enumerate(cases)), "stream must be ordered by t"
    return cases


# ── phase 1: store build ──────────────────────────────────────────────────────

def cmd_store(args):
    cases = load_stream(args.stream)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    open_defs = defs_text("open")

    dnames = args.dispute_models.split(",")
    dspecs = [resolve(m) for m in dnames]
    dclients = [make_client(s) for s in dspecs]

    # first pass is precedent-free -> parallel prefetch
    def one(job):
        i, mi = job
        try:
            tri, toks, _ = ground_tri(dclients[mi], dspecs[mi],
                                      cases[i]["narrative"], open_defs)
        except Exception as e:
            tri, toks = {a: "unknown" for a in GROUNDABLE}, 0
            print(f"first-pass error case {i} model {dnames[mi]}: {e}", file=sys.stderr)
        return i, mi, tri, toks
    jobs = [(i, mi) for i in range(len(cases)) for mi in range(len(dspecs))]
    firstpass, fp_toks = {}, 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for n_done, (i, mi, tri, toks) in enumerate(pool.map(one, jobs), 1):
            firstpass[(i, mi)] = tri
            fp_toks += toks
            if n_done % 50 == 0:
                print(f"first pass {n_done}/{len(jobs)}", file=sys.stderr)
    print(f"first pass done: {len(cases)} cases x {len(dspecs)} models, "
          f"{fp_toks} tokens", file=sys.stderr)

    # sequential adjudication (retrieval feeds back into the store)
    jspec = resolve(args.judge)
    judge = Adjudicator(make_client(jspec), jspec, LABELS, open_defs)
    store = Store(GROUNDABLE, args.embed)
    uni = Store(GROUNDABLE, args.embed) if args.uniform else None
    rng = random.Random(args.seed)
    uni_chosen: set[int] = set()
    j_toks = 0
    tok_lock = __import__("threading").Lock()

    def adjudicate_into(st: Store, case: dict, now_t: int, reasons: list[str]):
        nonlocal j_toks
        prec = st.retrieve(case["narrative"], args.k, "embed", before_t=now_t)
        adj = judge.adjudicate(case["narrative"], render_block(prec, LABELS))
        with tok_lock:
            j_toks += adj["tokens"]
        st.add({"case_id": case["case_id"], "t": now_t, "facts": case["narrative"],
                "findings": adj["findings"],
                "verdict": verdict_of(adj["findings"], case["acted"]),
                "rationale": adj["rationale"], "cites": adj["cites"],
                "retrieved": [p["case_id"] for p in prec],
                "judge": args.judge, "contested": reasons,
                "assign_key": case["assign_key"]})

    with open(out_dir / "disputes.jsonl", "w") as dlog:
        for i, case in enumerate(cases):
            tris = [firstpass[(i, mi)] for mi in range(len(dspecs))]
            vs = [verdict_of(t, case["acted"]) for t in tris]
            # A dispute is OUTCOME-level divergence (Priest-Klein: parties file
            # when their predicted outcomes differ). Unknown atoms alone are
            # honest epistemic gaps, recorded below but NOT a dispute trigger —
            # an unknown that matters flips a verdict; one that doesn't isn't
            # worth adjudicating.
            reasons = []
            if len({v["share_status"] for v in vs}) > 1:
                reasons.append("verdict_disagreement")
            if any(v["share_status"] == "unresolved" for v in vs):
                reasons.append("engine_unresolved")
            if reasons:
                print(f"adjudicating t={case['t']} ({'+'.join(reasons)}); "
                      f"store={len(store)}", file=sys.stderr)
                jobs = [(store, case, case["t"], reasons)]
                if uni is not None:   # matched accretion clock, uniform pick
                    avail = [j for j in range(i + 1) if j not in uni_chosen]
                    if avail:
                        j = rng.choice(avail)
                        uni_chosen.add(j)
                        jobs.append((uni, cases[j], case["t"], ["uniform"]))
                # the two adjudications are independent (different stores) —
                # run the pair concurrently to halve the sequential wall time
                with ThreadPoolExecutor(max_workers=2) as ex:
                    list(ex.map(lambda a: adjudicate_into(*a), jobs))
            dlog.write(json.dumps({
                "case_id": case["case_id"], "t": case["t"], "tier": case["tier"],
                "contested": bool(reasons), "reasons": reasons,
                "any_unknown": any("unknown" in t.values() for t in tris),
                "first_pass": {dnames[mi]: tris[mi] for mi in range(len(dspecs))},
                "first_verdicts": {dnames[mi]: vs[mi]["share_status"]
                                   for mi in range(len(dspecs))},
                "gold": case["gold"]["share_status"]}) + "\n")
            dlog.flush()

    store.save(out_dir / "store_precedent.jsonl")
    print(f"store_precedent: {len(store)} holdings "
          f"({len(store)}/{len(cases)} contested), consistency {store.consistency()}")
    if uni is not None:
        uni.save(out_dir / "store_uniform.jsonl")
        print(f"store_uniform:   {len(uni)} holdings, consistency {uni.consistency()}")
    print(f"judge tokens: {j_toks} ({judge.calls} calls, model {args.judge})")


# ── phase 2: evaluation ───────────────────────────────────────────────────────

def gold_store_from(cases: list[dict], embed_provider: str) -> Store:
    st = Store(GROUNDABLE, embed_provider)
    for c in cases:
        st.add({"case_id": c["case_id"], "t": c["t"], "facts": c["narrative"],
                "findings": {a: ("true" if v else "false")
                             for a, v in c["assignment"].items()},
                "verdict": c["gold"], "rationale": "", "cites": [],
                "judge": "gold", "contested": [], "assign_key": c["assign_key"]})
    return st


def gold_retrieve(gold: Store, case: dict, k: int) -> list[dict]:
    """Ceiling retrieval: same latent assignment first (most recent), embed
    backfill — the grounder gets genuinely relevant, correctly-labeled shots."""
    rel = sorted((h for h in gold.holdings
                  if h["t"] < case["t"] and h["assign_key"] == case["assign_key"]),
                 key=lambda h: -h["t"])[:k]
    if len(rel) < k:
        seen = {h["case_id"] for h in rel}
        for h in gold.retrieve(case["narrative"], k + len(rel), "embed",
                               before_t=case["t"]):
            if h["case_id"] not in seen:
                rel.append(h)
                if len(rel) == k:
                    break
    return rel


def run_case(case, arm, stores, client=None, spec=None, k=5):
    """One (case, arm) evaluation. Returns the result-row tail."""
    t0 = time.time()
    toks, raw, retrieved = 0, "", None
    tri = None
    if arm == "oracle":
        tri = {a: ("true" if v else "false") for a, v in case["assignment"].items()}
    elif arm == "program":
        present = {it["id"] for it in case["items"]}
        tri = {a: ("true" if CLOSED_IDS[a] & present else "false") for a in GROUNDABLE}
    elif arm.startswith("ground_"):
        regime = arm.removeprefix("ground_")
        tri, toks, raw = ground_tri(client, spec, case["narrative"], defs_text(regime))
    elif arm.startswith(("precedent", "uniform", "goldfs")):
        base = arm.split("@")[0]
        mode = arm.split("@")[1] if "@" in arm else "embed"
        st = stores[base]
        provisional = None
        if base != "goldfs" and mode in ("atom", "rule"):
            provisional, t1, r1 = ground_tri(client, spec, case["narrative"],
                                             defs_text("open"))
            toks += t1
            raw += f"[provisional] {r1}\n"
        if base == "goldfs":
            prec = gold_retrieve(st, case, k)
        else:
            prec = st.retrieve(case["narrative"], k, mode,
                               provisional=provisional, before_t=case["t"])
        retrieved = prec
        block = render_block(prec, LABELS, show_rationale=(base != "goldfs"))
        tri, t2, r2 = ground_tri(client, spec, case["narrative"],
                                 defs_text("open"), prec_block=block)
        toks += t2
        raw += r2
    else:
        raise ValueError(f"unknown arm: {arm}")

    row = {"pred_tri": tri,
           "pred_assignment": {a: tri[a] == "true" for a in GROUNDABLE},
           "pred_verdict": verdict_of(tri, case["acted"]),
           "tokens": toks, "secs": round(time.time() - t0, 2), "raw": raw}
    if retrieved is not None:
        base = arm.split("@")[0]
        st = stores[base]
        avail = sum(1 for h in st.holdings
                    if h["t"] < case["t"] and h["assign_key"] == case["assign_key"])
        row["retrieved"] = [h["case_id"] for h in retrieved]
        row["n_relevant_retrieved"] = sum(1 for h in retrieved
                                          if h["assign_key"] == case["assign_key"])
        row["n_relevant_available"] = avail
        row["store_size"] = sum(1 for h in st.holdings if h["t"] < case["t"])
    return row


def cmd_eval(args):
    cases = load_stream(args.stream)
    out_dir = Path(args.out_dir)
    stores = {"goldfs": gold_store_from(cases, args.embed)}
    for base, fname in (("precedent", "store_precedent.jsonl"),
                        ("uniform", "store_uniform.jsonl")):
        p = out_dir / fname
        if p.exists():
            stores[base] = Store.load(p, GROUNDABLE, args.embed)

    arms = args.arms.split(",")
    for arm in arms:
        base = arm.split("@")[0]
        if base in ("precedent", "uniform") and base not in stores:
            raise SystemExit(f"arm {arm} needs {out_dir}/store_{base}.jsonl — run the store phase first")

    names = args.models
    names = {"cheap_panel": ",".join(CHEAP_PANEL),
             "all": ",".join(FULL_PANEL)}.get(names, names)
    model_names = names.split(",")

    out_path = out_dir / args.out
    out = open(out_path, "w")
    n = 0
    for arm in arms:
        llm_arm = arm not in ("oracle", "program")
        for mname in (model_names if llm_arm else ["-"]):
            client = spec = None
            if llm_arm:
                spec = resolve(mname)
                client = make_client(spec)

            def one(case, arm=arm, client=client, spec=spec, mname=mname):
                try:
                    res = run_case(case, arm, stores, client, spec, k=args.k)
                except Exception as e:      # keep the sweep alive; scored wrong
                    res = {"pred_tri": None, "pred_assignment": None,
                           "pred_verdict": {"share_status": f"ERROR:{type(e).__name__}",
                                            "violation": False, "notify_required": False},
                           "tokens": 0, "secs": 0, "raw": str(e)[:300]}
                if arm == "oracle":
                    assert res["pred_verdict"] == case["gold"], \
                        f"ORACLE MISMATCH on {case['case_id']}"
                return {"case_id": case["case_id"], "t": case["t"],
                        "tier": case["tier"], "acted": case["acted"],
                        "assign_key": case["assign_key"], "arm": arm,
                        "model": mname, "gold": case["gold"],
                        "gold_assignment": case["assignment"], **res}

            with ThreadPoolExecutor(max_workers=args.workers if llm_arm else 1) as pool:
                for row in pool.map(one, cases):
                    out.write(json.dumps(row) + "\n")
                    out.flush()
                    n += 1
            print(f"done arm={arm} model={mname} ({len(cases)} cases)", file=sys.stderr)
    out.close()
    print(f"wrote {n} rows -> {out_path}")


# ── cli ───────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="phase", required=True)

    ps = sub.add_parser("store", help="build precedent (+ uniform) stores")
    ps.add_argument("--stream", default=str(HERE / "stream.jsonl"))
    ps.add_argument("--out-dir", default=str(HERE / "runs/e1"))
    ps.add_argument("--dispute-models", default="gpt-4.1,deepseek-v4-flash",
                    help="two cheap first-pass grounders (dispute detector)")
    ps.add_argument("--judge", default="claude-sonnet-5",
                    help="adjudicator model (the strong model deciding new cases)")
    ps.add_argument("--k", type=int, default=5)
    ps.add_argument("--workers", type=int, default=8)
    ps.add_argument("--seed", type=int, default=0)
    ps.add_argument("--embed", default="auto", choices=["auto", "openai", "offline"])
    ps.add_argument("--no-uniform", dest="uniform", action="store_false",
                    help="skip the matched uniform store (halves judge cost)")
    ps.set_defaults(func=cmd_store, uniform=True)

    pe = sub.add_parser("eval", help="run arms x models against frozen stores")
    pe.add_argument("--stream", default=str(HERE / "stream.jsonl"))
    pe.add_argument("--out-dir", default=str(HERE / "runs/e1"))
    pe.add_argument("--out", default="results_e1.jsonl")
    pe.add_argument("--arms", default="oracle,program,ground_closed,ground_open,"
                    "ground_hybrid,precedent@embed,uniform,goldfs")
    pe.add_argument("--models", default="stub",
                    help="comma list, or 'cheap_panel' / 'all'")
    pe.add_argument("--k", type=int, default=5)
    pe.add_argument("--workers", type=int, default=8)
    pe.add_argument("--embed", default="auto", choices=["auto", "openai", "offline"])
    pe.set_defaults(func=cmd_eval)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
