#!/usr/bin/env python3
"""Wilson 95% confidence intervals for the E1 headline numbers (n is small, so
normal-approx CIs are wrong near 0/1; Wilson is the right small-n interval).
Recomputes verdict acc, offence-ID acc, and pair acc per arm from predictions +
gold, with CIs, so the paper's table can carry honest error bars."""
import json, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = os.path.normpath(os.path.join(HERE, ".."))

ds = [json.loads(l) for l in open(os.path.join(EVAL, "dataset", "v0_pilot.jsonl"))]
gold = {it["id"]: it for it in ds}
preds = [json.loads(l) for l in open(os.path.join(EVAL, "results", "predictions.jsonl"))]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (p, max(0.0, c-h), min(1.0, c+h))


def fmt(k, n):
    p, lo, hi = wilson(k, n)
    return f"{k}/{n} = {p*100:4.0f}%  [95% CI {lo*100:.0f}–{hi*100:.0f}]"


for arm in ("deontic", "llm_only", "rag"):
    P = [p for p in preds if p["arm"] == arm]
    pv = {p["id"]: p for p in P}
    if not P:
        print(f"\n=== {arm}: (no rows) ==="); continue
    # verdict
    vk = sum(1 for p in P if p.get("pred_verdict") == gold[p["id"]]["gold"]["verdict"])
    vn = len(P)
    # offence-id (only items whose gold has an offence)
    off = [p for p in P if gold[p["id"]]["gold"].get("offence")]
    ok = sum(1 for p in off if p.get("pred_offence") == gold[p["id"]]["gold"]["offence"])
    on = len(off)
    # pair accuracy: both twins' verdicts correct
    pairs, seen = 0, set()
    pc = 0
    for p in P:
        it = gold[p["id"]]; mp = it.get("minimal_pair")
        if not mp or p["id"] in seen or mp in seen or mp not in pv:
            continue
        seen.add(p["id"]); seen.add(mp); pairs += 1
        a = p.get("pred_verdict") == it["gold"]["verdict"]
        b = pv[mp].get("pred_verdict") == gold[mp]["gold"]["verdict"]
        pc += 1 if (a and b) else 0
    print(f"\n=== {arm} ===")
    print(f"  verdict   : {fmt(vk, vn)}")
    print(f"  offence-ID: {fmt(ok, on)}")
    print(f"  pair-acc  : {fmt(pc, pairs)}")
