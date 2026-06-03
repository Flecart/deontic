"""Orchestration: run the four arms, log every round to JSONL, compute metrics.

  python -m freight.run --arms CL,Civ,US,RR --rounds 120 --seeds 0,1 \
      --judge-model gpt-4o-mini --out freight/runs

De-risk first (the corpus machinery alone, stub agents that file everything):

  python -m freight.run --arms CL --rounds 60 --agents stub --seeds 0

Arms differ only in how the corpus C accretes (see corpus.py). US and RR accrete
at a rate calibrated to CL's realised filing rate (measured per seed by running
CL first). Transfers (settlement r, damages d) cancel in total welfare, so the
welfare channel is: a more accurate corpus deters value-destroying deviation
(the seller anticipates liability) and provokes fewer wasteful disputes.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import statistics as st
import time

from . import env
from .agents import StrategicAgents, StubAgents, _precedent_prior, seller_deviation
from .corpus import Corpus, inject_random_rule, seed_civ
from .judge import Judge

TASK_DESCRIPTION = (
    "Buyers and sellers contract over freight shipments. Sellers may deviate from "
    "spec (quality, packaging, lateness, shortfall, substitution) under cost "
    "pressure. Decide breaches and damages so that the law deters value-destroying "
    "deviation while permitting commercially reasonable performance.")


# --- one arm, one seed ------------------------------------------------------

def run_arm(arm, rounds, seed, judge_model, embed_q, agents_kind, k, c_f, log_fp):
    rng = random.Random(seed * 7919 + hash(arm) % 1000)
    corpus = Corpus(arm)
    judge = Judge(corpus, model=judge_model, k=k)
    agents = StubAgents() if agents_kind == "stub" else StrategicAgents()

    if arm == "Civ":
        seed_civ(corpus, TASK_DESCRIPTION, judge_model)

    rows = []
    for t in range(rounds):
        # seller's physical choice: under a corpus, anticipate liability (the
        # strategic seller deviates less when precedent threatens damages).
        theta = env.cost_shock(rng)
        c = env.sample_contract(rng)
        if agents.strategic and len(corpus):
            dev = _best_deviation(c, theta, corpus, rng)
        else:
            dev = seller_deviation(theta, liability_aversion=0.0, rng=rng)
        d = env.choose_delivery(c, theta, rng, deviate=dev)
        txn = env.assemble(c, d, theta, env.valuation_noise(rng))

        c_f_abs = c_f * txn["price"]          # filing cost scales with the stakes
        decision = agents.interact(corpus, txn, c_f_abs, rng)
        row = {"t": t, "arm": arm, "seed": seed, "ambiguity": txn["ambiguity"],
               "severity": txn["severity"], "price": txn["price"],
               "oracle": txn["oracle"]["ruling"], **{k2: decision[k2] for k2 in
               ("filed", "settled", "r", "p_B", "p_S", "n_prec")}}

        ruling = None
        if decision["filed"]:
            ruling = judge.rule(txn)
            row["ruling"] = ruling["ruling"]
            row["damage"] = ruling["damage_abs"]
            row["win_plaintiff"] = int(ruling["ruling"] == "breach")
            if arm == "CL":                       # CL accretes only filed cases
                corpus.add(_to_case(txn, ruling, t))

        # US/RR accrete on their own schedule, regardless of the dispute above.
        # US submits THIS round's transaction (per spec: sample regardless of
        # dispute), so its accreted population matches the underlying draw -> the
        # KL selection axis is comparable to CL's.
        if arm == "US" and rng.random() < embed_q:
            sruling = ruling if ruling is not None else judge.rule(txn)
            corpus.add(_to_case(txn, sruling, t))
            row["us_sampled"] = {"ambiguity": txn["ambiguity"],
                                 "win_plaintiff": int(sruling["ruling"] == "breach")}
        elif arm == "RR" and rng.random() < embed_q:
            inject_random_rule(corpus, judge_model, rng)

        row["corpus_size"] = len(corpus)
        rows.append(row)
        log_fp.write(json.dumps(row) + "\n")

    return corpus, judge, rows


def _to_case(txn, ruling, t):
    return {"facts": txn["facts"], "ruling": ruling["ruling"],
            "damage": ruling["damage"], "rationale": ruling.get("rationale", ""),
            "ambiguity": txn["ambiguity"], "severity": txn["severity"],
            "permissiveness": txn["permissiveness"], "fm": txn["fm"], "t": t}


def _best_deviation(c, theta, corpus, rng):
    """Seller picks the deviation appetite maximising expected net payoff under
    the corpus prior: price - cost(dev) - P(breach|dev)*E[damage]*price."""
    best, best_u = 0.0, -1e18
    for g in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
        d = env.choose_delivery(c, theta, random.Random(hash((g, theta)) & 0xffff), deviate=g)
        txn = env.assemble(c, d, theta, 0.0)
        p, d_hat, _, _ = _precedent_prior(corpus, txn)
        u = c.price - env.cost(c, d, theta) - p * d_hat * c.price
        if u > best_u:
            best_u, best = u, g
    return best


# --- held-out evaluation of a terminal corpus -------------------------------

def make_heldout(n, seed):
    rng = random.Random(7_000_003 + seed)
    return [env.transaction(rng) for _ in range(n)]


def eval_welfare(heldout, corpus, c_f, rng):
    """Stake-weighted welfare under a terminal corpus: the seller re-optimises
    its deviation against this arm's law, then realised welfare = (v - c) minus
    wasteful dispute costs. Transfers cancel. Retrieval only -- no judge calls."""
    agents = StrategicAgents()
    total = 0.0
    for s in heldout:
        c = s["_c"]
        theta, eta = s["theta"], s["eta"]
        g = _best_deviation(c, theta, corpus, rng) if len(corpus) else \
            seller_deviation(theta, 0.0, rng)
        d = env.choose_delivery(c, theta, random.Random(hash((g, theta)) & 0xffff), deviate=g)
        txn = env.assemble(c, d, theta, eta)
        c_f_abs = c_f * txn["price"]
        dec = agents.interact(corpus, txn, c_f_abs, rng)
        w = txn["value"] - txn["cost"] - (c_f_abs if dec["filed"] else 0.0)
        total += w
    return round(total, 2)


def eval_accuracy(heldout, corpus, judge, frac_labelled=0.3):
    """Stake-weighted accuracy of J (under terminal C) vs the UCC oracle, on a
    labelled subset. Weight by price (stake)."""
    lab = heldout[:max(1, int(len(heldout) * frac_labelled))]
    num = den = 0.0
    for s in lab:
        r = judge.rule(s)["ruling"]
        w = s["price"]
        den += w
        num += w * (r == s["oracle"]["ruling"])
    return round(num / den, 3) if den else float("nan")


def eval_consistency(heldout, judge, n_cases=5, n_resample=3):
    vals = [judge.self_consistency(s, n=n_resample) for s in heldout[:n_cases]]
    vals = [v for v in vals if not math.isnan(v)]
    return round(st.mean(vals), 3) if vals else float("nan")


# --- metrics over the round log ---------------------------------------------

def _winrate_trajectory(rows, window=20):
    filed = [(r["t"], r.get("win_plaintiff")) for r in rows
             if r.get("filed") and "win_plaintiff" in r]
    out = []
    for i in range(0, len(filed), window):
        chunk = [w for _, w in filed[i:i + window]]
        if chunk:
            out.append(round(sum(chunk) / len(chunk), 3))
    return out, (round(st.mean([w for _, w in filed]), 3) if filed else None)


def _filing_trajectory(rows, window=20):
    out = []
    for i in range(0, len(rows), window):
        chunk = rows[i:i + window]
        out.append(round(sum(bool(r.get("filed")) for r in chunk) / len(chunk), 3))
    return out


def _kl_ambiguity(all_amb, acc_amb, bins=5):
    """KL(accreted || all) along the ambiguity axis -- selection-bias measure."""
    if not acc_amb:
        return 0.0
    edges = [i / bins for i in range(bins + 1)]

    def hist(xs):
        h = [0.0] * bins
        for x in xs:
            b = min(bins - 1, int(x * bins))
            h[b] += 1
        tot = sum(h) or 1.0
        return [(c + 0.5) / (tot + 0.5 * bins) for c in h]   # Laplace-smoothed
    p, q = hist(acc_amb), hist(all_amb)
    return round(sum(pi * math.log(pi / qi) for pi, qi in zip(p, q)), 4)


# --- driver -----------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", default="CL,Civ,US,RR")
    ap.add_argument("--rounds", type=int, default=120)
    ap.add_argument("--seeds", default="0,1")
    ap.add_argument("--agents", choices=["strategic", "stub"], default="strategic")
    ap.add_argument("--judge-model", default="gpt-4o-mini")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--c-f", type=float, default=0.06,
                    help="filing cost as a fraction of contract price (stake-scaled)")
    ap.add_argument("--heldout", type=int, default=40)
    ap.add_argument("--out", default=os.path.dirname(__file__) + "/runs")
    args = ap.parse_args()

    arms = args.arms.split(",")
    seeds = [int(s) for s in args.seeds.split(",")]
    os.makedirs(args.out, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    summary = {"config": vars(args), "stamp": stamp, "runs": []}

    for seed in seeds:
        heldout = make_heldout(args.heldout, seed)
        cl_rate = None
        for arm in arms:
            # calibrate US/RR accretion to CL's filing rate (this seed).
            q = cl_rate if arm in ("US", "RR") and cl_rate is not None else 0.5
            log_path = os.path.join(args.out, f"{stamp}_{arm}_s{seed}.jsonl")
            t0 = time.time()
            with open(log_path, "w") as fp:
                corpus, judge, rows = run_arm(
                    arm, args.rounds, seed, args.judge_model, q,
                    args.agents, args.k, args.c_f, fp)

            if arm == "CL":
                cl_rate = round(sum(bool(r.get("filed")) for r in rows) / len(rows), 3)

            traj_win, win_overall = _winrate_trajectory(rows)
            fwins = [r["win_plaintiff"] for r in rows
                     if r.get("filed") and "win_plaintiff" in r]
            third = max(1, len(rows) // 3)
            win_late = (round(st.mean(fwins[len(fwins) // 2:]), 3)
                        if len(fwins) >= 4 else None)
            file_early = round(sum(bool(r.get("filed")) for r in rows[:third]) / third, 3)
            file_late = round(sum(bool(r.get("filed")) for r in rows[-third:]) / third, 3)
            all_amb = [r["ambiguity"] for r in rows]
            acc_amb = [c["ambiguity"] for c in corpus.cases
                       if not c.get("is_rule") and not c.get("is_code")]
            rec = {
                "arm": arm, "seed": seed, "log": os.path.basename(log_path),
                "wall_s": round(time.time() - t0, 1), "judge_calls": judge.calls,
                "corpus_size": len(corpus),
                "filing_rate": round(sum(bool(r.get("filed")) for r in rows) / len(rows), 3),
                "filing_trajectory": _filing_trajectory(rows),
                "filing_early": file_early, "filing_late": file_late,
                "winrate_trajectory": traj_win, "winrate_overall": win_overall,
                "winrate_late": win_late,
                "kl_selection": _kl_ambiguity(all_amb, acc_amb),
                "mean_ambiguity_accreted": round(st.mean(acc_amb), 3) if acc_amb else None,
                "mean_ambiguity_all": round(st.mean(all_amb), 3),
                "closure": corpus.closure_conflicts(),
                "welfare": eval_welfare(heldout, corpus, args.c_f, random.Random(seed)),
                "accuracy_vs_oracle": eval_accuracy(heldout, corpus, judge),
                "predictability": eval_consistency(heldout, judge),
            }
            summary["runs"].append(rec)
            print(f"[{arm} s{seed}] |C|={rec['corpus_size']} "
                  f"file={rec['filing_rate']} win={rec['winrate_overall']} "
                  f"KL={rec['kl_selection']} W={rec['welfare']} "
                  f"acc={rec['accuracy_vs_oracle']} consist={rec['predictability']} "
                  f"calls={rec['judge_calls']} ({rec['wall_s']}s)", flush=True)

    spath = os.path.join(args.out, f"{stamp}_summary.json")
    with open(spath, "w") as fp:
        json.dump(summary, fp, indent=2)
    print("\nsummary ->", spath)
    return spath


if __name__ == "__main__":
    main()
