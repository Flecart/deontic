"""E1 scorer: tables from results_e1.jsonl (markdown to stdout).

  1. verdict accuracy by arm[model] x tier
  2. accuracy vs stream time (terciles) — the consistency-slope check
  3. the E1 gate numbers: X = fraction of the closed<->open Tier-0/1 gap the
     precedent arm closes; Y = fraction of open's Tier-2 advantage it retains
     (plan proposes X>=70%, Y>=90%; computed on the last tercile, where the
     store is mature)
  4. retrieval quality vs gold relevance (P@k, hit@k) per retrieval arm
  5. inter-model agreement (mean pairwise Cohen's kappa on verdicts) per arm,
     by tercile — the epistemic-coordination curve
  6. store / dispute diagnostics if disputes.jsonl sits next to the results

Usage: python e1_score.py --results runs/e1/results_e1.jsonl [--exclude-leaky stream.jsonl]
"""
from __future__ import annotations
import argparse, itertools, json
from collections import defaultdict
from pathlib import Path


def pct(num, den):
    return f"{100*num/den:5.1f}% ({num}/{den})" if den else "    -"


def _acc(rows):
    n = len(rows)
    ok = sum(r["pred_verdict"]["share_status"] == r["gold"]["share_status"] for r in rows)
    return ok, n


def kappa(pairs):
    """Cohen's kappa over a list of (label_a, label_b)."""
    n = len(pairs)
    if not n:
        return float("nan")
    po = sum(a == b for a, b in pairs) / n
    labels = {l for p in pairs for l in p}
    pe = sum((sum(a == l for a, _ in pairs) / n) * (sum(b == l for _, b in pairs) / n)
             for l in labels)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--exclude-leaky", default=None,
                    help="stream.jsonl; drop cases with non-empty leak_flags")
    args = ap.parse_args()

    rows = [json.loads(l) for l in Path(args.results).read_text().splitlines() if l]
    if args.exclude_leaky:
        leaky = {json.loads(l)["case_id"]
                 for l in Path(args.exclude_leaky).read_text().splitlines()
                 if l and json.loads(l)["leak_flags"]}
        rows = [r for r in rows if r["case_id"] not in leaky]
        print(f"_(excluded {len(leaky)} leak-flagged cases)_\n")

    T = max(r["t"] for r in rows) + 1
    tercile = lambda t: min(2, 3 * t // T)
    key_of = lambda r: r["arm"] + (f"[{r['model']}]" if r["model"] != "-" else "")
    tiers = sorted({r["tier"] for r in rows})
    by_arm = defaultdict(list)
    for r in rows:
        by_arm[key_of(r)].append(r)

    # 1. accuracy by arm x tier
    print("## Verdict accuracy by arm x tier\n")
    print("| arm | " + " | ".join(f"tier {t}" for t in tiers) + " | all |")
    print("|---|" + "---|" * (len(tiers) + 1))
    for a in sorted(by_arm):
        cells = [pct(*_acc([r for r in by_arm[a] if r["tier"] == t])) for t in tiers]
        print(f"| {a} | " + " | ".join(cells) + f" | {pct(*_acc(by_arm[a]))} |")

    # 2. accuracy vs time
    print("\n## Verdict accuracy by stream tercile (all tiers pooled)\n")
    print("| arm | early | mid | late | slope late-early |")
    print("|---|---|---|---|---|")
    for a in sorted(by_arm):
        accs = []
        for b in range(3):
            ok, n = _acc([r for r in by_arm[a] if tercile(r["t"]) == b])
            accs.append(ok / n if n else float("nan"))
        cells = [f"{100*x:5.1f}%" for x in accs]
        print(f"| {a} | " + " | ".join(cells) + f" | {100*(accs[2]-accs[0]):+5.1f}pp |")

    # 3. gate numbers (per model that ran all three of open/closed/precedent)
    prec_arms = sorted({r["arm"] for r in rows if r["arm"].startswith("precedent")})
    models = sorted({r["model"] for r in rows if r["model"] != "-"})
    gate_lines = []
    for m, pa in itertools.product(models, prec_arms):
        def acc_of(arm, pred, model=m):
            sel = [r for r in rows if r["arm"] == arm and r["model"] == model
                   and pred(r) and tercile(r["t"]) == 2]
            ok, n = _acc(sel)
            return ok / n if n else None
        t01 = lambda r: r["tier"] in (0, 1)
        t2 = lambda r: r["tier"] == 2
        c01, o01, p01 = acc_of("ground_closed", t01), acc_of("ground_open", t01), acc_of(pa, t01)
        c2, o2, p2 = acc_of("ground_closed", t2), acc_of("ground_open", t2), acc_of(pa, t2)
        if None in (c01, o01, p01, c2, o2, p2):
            continue
        x = f"{100*(p01 - o01)/(c01 - o01):5.1f}%" if c01 != o01 else "n/a (no gap)"
        y = f"{100*(p2 - c2)/(o2 - c2):5.1f}%" if o2 != c2 else "n/a (no gap)"
        gate_lines.append(f"| {m} | {pa} | {x} | {y} | "
                          f"{100*c01:.1f}/{100*o01:.1f}/{100*p01:.1f} | "
                          f"{100*c2:.1f}/{100*o2:.1f}/{100*p2:.1f} |")
    if gate_lines:
        print("\n## E1 gate (last tercile): X = gap closed (T0/1), Y = T2 advantage kept\n")
        print("| model | arm | X | Y | closed/open/prec T0-1 | closed/open/prec T2 |")
        print("|---|---|---|---|---|---|")
        print("\n".join(gate_lines))
        print("\n_(proposed gate: X >= 70%, Y >= 90%)_")

    # 4. retrieval quality
    ret = [r for r in rows if r.get("retrieved") is not None]
    if ret:
        print("\n## Retrieval vs gold relevance (rows with >=1 relevant available)\n")
        print("| arm | P@k | hit@k | mean store size | n |")
        print("|---|---|---|---|---|")
        stats = defaultdict(list)
        for r in ret:
            if r.get("n_relevant_available", 0) > 0 and r["retrieved"]:
                stats[key_of(r)].append(r)
        for a in sorted(stats):
            rs = stats[a]
            p = sum(r["n_relevant_retrieved"] / len(r["retrieved"]) for r in rs) / len(rs)
            hit = sum(r["n_relevant_retrieved"] > 0 for r in rs)
            sz = sum(r.get("store_size", 0) for r in rs) / len(rs)
            print(f"| {a} | {100*p:5.1f}% | {pct(hit, len(rs))} | {sz:5.1f} | {len(rs)} |")

    # 5. inter-model agreement per arm x tercile
    arms_multi = sorted({r["arm"] for r in rows
                         if r["model"] != "-" and len({x["model"] for x in rows
                                                       if x["arm"] == r["arm"]}) >= 2})
    if arms_multi:
        print("\n## Inter-model agreement (mean pairwise Cohen's kappa on verdicts)\n")
        print("| arm | early | mid | late |")
        print("|---|---|---|---|")
        for arm in arms_multi:
            preds = defaultdict(dict)   # (case_id) -> {model: verdict}
            terc = {}
            for r in rows:
                if r["arm"] == arm and r["model"] != "-":
                    preds[r["case_id"]][r["model"]] = r["pred_verdict"]["share_status"]
                    terc[r["case_id"]] = tercile(r["t"])
            ms = sorted({m for v in preds.values() for m in v})
            cells = []
            for b in range(3):
                ks = []
                for m1, m2 in itertools.combinations(ms, 2):
                    pairs = [(v[m1], v[m2]) for c, v in preds.items()
                             if terc[c] == b and m1 in v and m2 in v]
                    if pairs:
                        ks.append(kappa(pairs))
                cells.append(f"{sum(ks)/len(ks):.3f}" if ks else "-")
            print(f"| {arm} | " + " | ".join(cells) + " |")

    # 6. store diagnostics
    dpath = Path(args.results).parent / "disputes.jsonl"
    if dpath.exists():
        drows = [json.loads(l) for l in dpath.read_text().splitlines() if l]
        print("\n## Dispute / accretion diagnostics\n")
        print("| tercile | dispute rate | reasons (top) |")
        print("|---|---|---|")
        for b in range(3):
            sel = [d for d in drows if tercile(d["t"]) == b]
            reasons = defaultdict(int)
            for d in sel:
                for x in d["reasons"]:
                    reasons[x] += 1
            top = ", ".join(f"{k}:{v}" for k, v in
                            sorted(reasons.items(), key=lambda kv: -kv[1])[:3])
            print(f"| {b} | {pct(sum(d['contested'] for d in sel), len(sel))} | {top} |")


if __name__ == "__main__":
    main()
