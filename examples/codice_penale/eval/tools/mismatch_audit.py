#!/usr/bin/env python3
"""E2' (offline) — audit the llm_only arm's offence-ID *mistakes* against the
engine gold, using data already on disk (no API). For each mismatch we print the
story, the gold offence, the offence the single-pass LLM picked, and the LLM's
own stated reason. The debate then judges whether the LLM's wrong picks are
legally indefensible (=> engine gold is correct, circularity broken) or merely
defensible alternatives (=> gold is contestable)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
EVAL = os.path.normpath(os.path.join(HERE, ".."))

ds = [json.loads(l) for l in open(os.path.join(EVAL, "dataset", "v0_pilot.jsonl"))]
gold = {it["id"]: it for it in ds}
preds = [json.loads(l) for l in open(os.path.join(EVAL, "results", "predictions.jsonl"))]
llm_only = [p for p in preds if p["arm"] == "llm_only"]

mm = 0
for p in llm_only:
    it = gold[p["id"]]
    g = it["gold"].get("offence")
    if not g:
        continue
    pred = p.get("pred_offence")
    if pred != g:
        mm += 1
        narr = " ".join(it["narrative"].split())
        print("--- {}  GOLD={}  LLM_PICKED={}".format(p["id"], g, pred))
        print("    story: " + narr[:170])
        raw = p.get("raw", "")
        try:
            r = json.loads(raw)
            print("    llm_reason: " + str(r.get("reason")))
        except Exception:
            print("    raw: " + str(raw)[:150])
print("\n# llm_only offence-ID mismatches: {}".format(mm))
