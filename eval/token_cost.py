#!/usr/bin/env python3
"""Token + cost accounting for reproducing the benchmark, straight from logs.

Token counts are EXACT: summed from the `tokens` field (prompt+completion) that
arms.py records on every LLM call. Dollar figures are estimates — edit PRICE
(blended $/1M total tokens per model) to match live pricing, then re-run.

  python token_cost.py            # core (3 families) + full breakdown
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent

# Blended $ per 1M tokens (prompt+completion combined). ROUGH — verify live.
PRICE = {
    "gpt-4.1":            3.0,
    "gpt-5.4":           10.0,   # reasoning model: hidden reasoning tokens inflate this
    "deepseek-v4-flash":  0.25,
    "qwen3.6-plus":       0.40,
    "narrator":           6.0,   # claude-sonnet-4.6, ~half output
    "annotator":          1.5,   # mixed cheap families for bank validation
}

CORE_FAMILIES = {"gpt-4.1", "deepseek-v4-flash", "qwen3.6-plus"}
CORE_ARMS = {"ground_closed", "ground_open", "holistic"}

MAIN = ["expA/results_stage2_main.jsonl", "expB/results_main.jsonl",
        "expC/results.jsonl", "expD/results_main.jsonl",
        "expE/results_main.jsonl", "expF/results_main.jsonl"]
EXTRA = ["expA/results_stage2_extras.jsonl", "expA/results_stage2_holclosed.jsonl",
         "expA/results_stage2_open2_gpt54.jsonl", "expA/results_stage2_ruling.jsonl",
         "expB/results_extras.jsonl", "expB/results_open2_gpt54.jsonl",
         "expB/results_holclosed.jsonl", "expB/results_advocacy.jsonl",
         "expD/results_reground.jsonl"]
CASE_FILES = [("expA", "cases_stage2_memo.jsonl"), ("expB", "cases_memo.jsonl"),
              ("expC", "cases.jsonl"), ("expD", "cases_memo.jsonl"),
              ("expE", "cases_memo.jsonl"), ("expF", "cases_memo.jsonl")]


def sum_tokens(files, arms=None, fams=None):
    tok = defaultdict(int)
    for f in files:
        p = HERE / f
        if not p.exists():
            continue
        for l in p.open():
            r = json.loads(l)
            if not r.get("tokens"):
                continue
            if arms and r["arm"] not in arms:
                continue
            if fams and r.get("model") not in fams:
                continue
            tok[r.get("model", "?")] += r["tokens"]
    return tok


def cost(tok, label_price=None):
    return sum(t / 1e6 * PRICE.get(label_price or m, 0) for m, t in tok.items())


def show(title, tok, price_key=None):
    total_tok = sum(tok.values())
    total_cost = sum(t / 1e6 * PRICE.get(price_key or m, 0) for m, t in tok.items())
    print(f"\n{title}")
    for m in sorted(tok, key=lambda x: -tok[x]):
        pk = price_key or m
        print(f"  {m:18s} {tok[m]/1e6:6.2f} M  ${tok[m]/1e6*PRICE.get(pk,0):6.2f}")
    print(f"  {'subtotal':18s} {total_tok/1e6:6.2f} M  ${total_cost:6.2f}")
    return total_tok / 1e6, total_cost


def main():
    ncases = sum(sum(1 for _ in (HERE / d / f).open()) for d, f in CASE_FILES)
    narr_tok = ncases * 550 / 1e6          # ~550 tok/case incl. leak-retries
    val_tok = 6 * 100 * 2 * 320 / 1e6       # 6 statutes x ~100 items x 2 annotators

    print("="*52, "\nCORE reproduction (3 families, main arms, no gpt-5.4)\n" + "="*52)
    core = sum_tokens(MAIN, CORE_ARMS, CORE_FAMILIES)
    ct, cc = show("arms:", core)
    print(f"\n  narration   {narr_tok:6.2f} M  ${narr_tok*PRICE['narrator']:6.2f}  ({ncases} cases)")
    print(f"  validation  {val_tok:6.2f} M  ${val_tok*PRICE['annotator']:6.2f}")
    core_total = cc + narr_tok*PRICE['narrator'] + val_tok*PRICE['annotator']
    print(f"  >>> CORE TOTAL: {ct+narr_tok+val_tok:.1f} M tokens, ~${core_total:.0f}")

    print("\n" + "="*52, "\nFULL reproduction (4 families + all secondary runs)\n" + "="*52)
    allrows = sum_tokens(MAIN + EXTRA)
    at, ac = show("all arm tokens:", allrows)
    full_narr = narr_tok * 1.6             # + advocacy + ruling re-narrations
    full_total = ac + full_narr*PRICE['narrator'] + val_tok*PRICE['annotator']
    print(f"\n  narration   {full_narr:6.2f} M  ${full_narr*PRICE['narrator']:6.2f}")
    print(f"  validation  {val_tok:6.2f} M  ${val_tok*PRICE['annotator']:6.2f}")
    print(f"  >>> FULL TOTAL: {at+full_narr+val_tok:.1f} M tokens, ~${full_total:.0f}")
    g5 = sum_tokens(MAIN + EXTRA, fams={"gpt-5.4"})
    print(f"  (of which gpt-5.4: {sum(g5.values())/1e6:.1f} M, ~${cost(g5):.0f} "
          f"-- ~{100*cost(g5)/full_total:.0f}% of full cost, the strongest-model analyses only)")
    print("\nToken counts are exact (from logs); $ are estimates -- edit PRICE and re-run.")


if __name__ == "__main__":
    main()
