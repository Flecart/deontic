"""Paper figure: the generalization curve + the ex-ante/ex-post economics.

All numbers are recomputed from eval/expA/results_stage2_main.jsonl and
results_stage2_extras.jsonl (leak-excluded population, 287 cases), atom-level
accuracy. Run from repo root:

    .venv/bin/python paper/figures/make_figures.py
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
EXPA = ROOT / "eval" / "expA"
OUT = Path(__file__).resolve().parent

CLOSED_C = "#C44E52"
OPEN_C = "#4C72B0"
PROGRAM_C = "#222222"


def leaky_cases() -> set[str]:
    cases = [json.loads(l) for l in (EXPA / "cases_stage2_memo.jsonl").open()]
    return {c["case_id"] for c in cases if c.get("leak_flags")}


def atom_acc(path: Path, leaky: set[str]):
    """(arm, model) -> tier -> accuracy% over all 7 atoms."""
    hits = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0]))
    for line in path.open():
        r = json.loads(line)
        if r["case_id"] in leaky or r.get("pred_assignment") is None:
            continue
        k, t = (r["arm"], r.get("model")), r["tier"]
        for atom, gold in r["gold_assignment"].items():
            hits[k][t][0] += int(r["pred_assignment"].get(atom) == gold)
            hits[k][t][1] += 1
    return {
        k: {t: 100.0 * c / n for t, (c, n) in tiers.items()}
        for k, tiers in hits.items()
    }


def pooled(acc, arm, models):
    return [
        sum(acc[(arm, m)][t] for m in models) / len(models) for t in (0, 1, 2)
    ]


def main() -> None:
    leaky = leaky_cases()
    acc = atom_acc(EXPA / "results_stage2_main.jsonl", leaky)
    extras = atom_acc(EXPA / "results_stage2_extras.jsonl", leaky)
    models = ["deepseek-v4-flash", "gpt-4.1", "gpt-5.4", "qwen3.6-plus"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.7))
    tiers = [0, 1, 2]

    # (a) generalization curve -------------------------------------------
    for m in models:
        ax1.plot(tiers, [acc[("ground_closed", m)][t] for t in tiers],
                 color=CLOSED_C, alpha=0.3, lw=0.9)
        ax1.plot(tiers, [acc[("ground_open", m)][t] for t in tiers],
                 color=OPEN_C, alpha=0.3, lw=0.9)
    ax1.plot(tiers, pooled(acc, "ground_closed", models), color=CLOSED_C,
             lw=2.2, marker="o", ms=4.5, label="closed (extensional) + LLM")
    ax1.plot(tiers, pooled(acc, "ground_open", models), color=OPEN_C,
             lw=2.2, marker="o", ms=4.5, label="open (intensional) + LLM")
    ax1.plot(tiers, [acc[("program", "-")][t] for t in tiers], color=PROGRAM_C,
             lw=1.8, ls="--", marker="s", ms=4.5, label="program (no LLM)")
    ax1.set_xticks(tiers)
    ax1.set_xticklabels(["tier 0\n(listed)", "tier 1\n(near-variant)",
                         "tier 2\n(world shift)"], fontsize=7.5)
    ax1.set_ylabel("atom-level accuracy (%)", fontsize=8)
    ax1.set_ylim(33, 103)
    ax1.legend(fontsize=7, loc="lower left", frameon=False)
    ax1.set_title("(a) Accuracy under instance novelty", fontsize=9)

    # (b) ex-ante drafting effort vs ex-post interpretation --------------
    ks = [2, 4, 8]  # 8 = full enumeration (3-8 categories per atom)
    t0 = [extras[("ground_closed@2", "gpt-4.1")][0],
          extras[("ground_closed@4", "gpt-4.1")][0],
          acc[("ground_closed", "gpt-4.1")][0]]
    t2 = [extras[("ground_closed@2", "gpt-4.1")][2],
          extras[("ground_closed@4", "gpt-4.1")][2],
          acc[("ground_closed", "gpt-4.1")][2]]
    open_t2 = acc[("ground_open", "gpt-4.1")][2]

    ax2.plot(ks, t0, color=CLOSED_C, lw=2.0, marker="o", ms=4.5,
             label="closed, tier 0 (in-distribution)")
    ax2.plot(ks, t2, color=CLOSED_C, lw=2.0, ls=":", marker="^", ms=4.5,
             label="closed, tier 2 (novel)")
    ax2.axhline(open_t2, color=OPEN_C, lw=2.0, ls="--")
    ax2.text(2.0, open_t2 + 1.2, "open intension, tier 2 (zero enumeration)",
             color=OPEN_C, fontsize=7, ha="left", va="bottom")
    ax2.annotate("drafting buys ~9 pts\nin-distribution",
                 xy=(7.85, t0[-1] + 0.8), xytext=(4.4, 97.0), fontsize=7,
                 arrowprops=dict(arrowstyle="->", lw=0.7))
    ax2.annotate("~0 pts out-of-distribution",
                 xy=(7.85, t2[-1] - 1.0), xytext=(4.1, 62.5), fontsize=7,
                 arrowprops=dict(arrowstyle="->", lw=0.7))
    ax2.set_xticks(ks)
    ax2.set_xticklabels(["K=2", "K=4", "full"], fontsize=8)
    ax2.set_xlabel("enumeration size (categories per atom)", fontsize=8)
    ax2.set_ylim(50, 103)
    ax2.legend(fontsize=7, loc="lower left", frameon=False)
    ax2.set_title("(b) What ex-ante drafting effort buys (gpt-4.1)",
                  fontsize=9)

    for ax in (ax1, ax2):
        ax.tick_params(labelsize=7.5)
        ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUT / "generalization_economics.pdf")
    fig.savefig(OUT / "generalization_economics.png", dpi=200)
    print("wrote", OUT / "generalization_economics.pdf")


if __name__ == "__main__":
    main()


# ── Figure 2: replication on the commons statute (expB) ─────────────────────

EXPB = ROOT / "eval" / "expB"


def leaky_cases_b() -> set[str]:
    cases = [json.loads(l) for l in (EXPB / "cases_memo.jsonl").open()]
    return {c["case_id"] for c in cases if c.get("leak_flags")}


def make_expb_figure() -> None:
    leaky = leaky_cases_b()
    acc = atom_acc(EXPB / "results_main.jsonl", leaky)
    extras = atom_acc(EXPB / "results_extras.jsonl", leaky)
    models = ["deepseek-v4-flash", "gpt-4.1", "gpt-5.4", "qwen3.6-plus"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.7))
    tiers = [0, 1, 2]

    for m in models:
        ax1.plot(tiers, [acc[("ground_closed", m)][t] for t in tiers],
                 color=CLOSED_C, alpha=0.3, lw=0.9)
        ax1.plot(tiers, [acc[("ground_open", m)][t] for t in tiers],
                 color=OPEN_C, alpha=0.3, lw=0.9)
    ax1.plot(tiers, pooled(acc, "ground_closed", models), color=CLOSED_C,
             lw=2.2, marker="o", ms=4.5, label="closed (extensional) + LLM")
    ax1.plot(tiers, pooled(acc, "ground_open", models), color=OPEN_C,
             lw=2.2, marker="o", ms=4.5, label="open (intensional) + LLM")
    ax1.plot(tiers, [acc[("program", "-")][t] for t in tiers], color=PROGRAM_C,
             lw=1.8, ls="--", marker="s", ms=4.5, label="program (no LLM)")
    ax1.set_xticks(tiers)
    ax1.set_xticklabels(["tier 0\n(listed)", "tier 1\n(near-variant)",
                         "tier 2\n(world shift)"], fontsize=7.5)
    ax1.set_ylabel("atom-level accuracy (%)", fontsize=8)
    ax1.set_ylim(33, 103)
    ax1.legend(fontsize=7, loc="lower left", frameon=False)
    ax1.set_title("(a) Commons statute: accuracy under novelty", fontsize=9)

    ks = [2, 4, 8]
    t0 = [extras[("ground_closed@2", "gpt-4.1")][0],
          extras[("ground_closed@4", "gpt-4.1")][0],
          acc[("ground_closed", "gpt-4.1")][0]]
    t2 = [extras[("ground_closed@2", "gpt-4.1")][2],
          extras[("ground_closed@4", "gpt-4.1")][2],
          acc[("ground_closed", "gpt-4.1")][2]]
    open_t2 = acc[("ground_open", "gpt-4.1")][2]

    ax2.plot(ks, t0, color=CLOSED_C, lw=2.0, marker="o", ms=4.5,
             label="closed, tier 0 (in-distribution)")
    ax2.plot(ks, t2, color=CLOSED_C, lw=2.0, ls=":", marker="^", ms=4.5,
             label="closed, tier 2 (novel)")
    ax2.axhline(open_t2, color=OPEN_C, lw=2.0, ls="--")
    ax2.text(2.0, open_t2 + 1.2, "open intension, tier 2 (zero enumeration)",
             color=OPEN_C, fontsize=7, ha="left", va="bottom")
    ax2.annotate("gist dividend:\n+10.9 by K=4",
                 xy=(4, t2[1] - 1.0), xytext=(2.2, 55), fontsize=7,
                 arrowprops=dict(arrowstyle="->", lw=0.7))
    ax2.annotate("then ~0",
                 xy=(7.85, t2[-1] - 1.0), xytext=(6.3, 62), fontsize=7,
                 arrowprops=dict(arrowstyle="->", lw=0.7))
    ax2.set_xticks(ks)
    ax2.set_xticklabels(["K=2", "K=4", "full"], fontsize=8)
    ax2.set_xlabel("enumeration size (categories per atom)", fontsize=8)
    ax2.set_ylim(50, 103)
    ax2.legend(fontsize=7, loc="lower right", frameon=False)
    ax2.set_title("(b) Commons statute: drafting sweep (gpt-4.1)",
                  fontsize=9)

    for ax in (ax1, ax2):
        ax.tick_params(labelsize=7.5)
        ax.spines[["top", "right"]].set_visible(False)

    fig.tight_layout()
    fig.savefig(OUT / "cross_statute.pdf")
    fig.savefig(OUT / "cross_statute.png", dpi=200)
    print("wrote", OUT / "cross_statute.pdf")


if __name__ == "__main__":
    make_expb_figure()


# ── Figure 3: cross-statute aggregate (6 statutes, 3 families) ───────────────

def make_aggregate_figure():
    import subprocess, re
    # per-statute Tier-2 gaps + pooled curve (hardcoded from eval/aggregate.py)
    statutes = ["A\ntransfer", "B\ncommons", "C\npark", "D\nagency", "E\nsale", "F\nsafety"]
    gaps = [14.8, 10.8, 20.8, 6.5, -0.3, -5.4]
    pooled_closed = [91.6, 84.4, 80.1]
    pooled_open = [82.7, 82.2, 83.0]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.7))
    tiers = [0, 1, 2]
    # (a) pooled closed-decays / open-flat crossover
    ax1.plot(tiers, pooled_closed, color=CLOSED_C, lw=2.4, marker="o", ms=5,
             label="closed (extensional)")
    ax1.plot(tiers, pooled_open, color=OPEN_C, lw=2.4, marker="o", ms=5,
             label="open (intensional)")
    ax1.fill_between(tiers, pooled_closed, pooled_open, where=[c > o for c, o in zip(pooled_closed, pooled_open)],
                     color=CLOSED_C, alpha=0.08)
    ax1.set_xticks(tiers)
    ax1.set_xticklabels(["tier 0\n(listed)", "tier 1", "tier 2\n(world shift)"], fontsize=7.5)
    ax1.set_ylabel("atom accuracy (%), 6 statutes pooled", fontsize=7.5)
    ax1.set_ylim(76, 94)
    ax1.legend(fontsize=7.5, loc="upper right", frameon=False)
    ax1.set_title("(a) Pooled: closed decays, open flat", fontsize=9)
    ax1.annotate("crossover", xy=(1.55, 82.6), xytext=(1.55, 79.0), fontsize=7,
                 ha="center", arrowprops=dict(arrowstyle="->", lw=0.6))
    # (b) per-statute Tier-2 gap spectrum
    colors = [OPEN_C if g > 0 else CLOSED_C for g in gaps]
    ax2.bar(range(len(statutes)), gaps, color=colors, alpha=0.85)
    ax2.axhline(0, color="#444444", lw=0.8)
    ax2.set_xticks(range(len(statutes)))
    ax2.set_xticklabels(statutes, fontsize=7)
    ax2.set_ylabel("Tier-2 open$-$closed gap (pts)", fontsize=7.5)
    ax2.set_title("(b) Gap varies by predicate texture", fontsize=9)
    ax2.text(1.0, 17.5, "artifact +\nspecific enums", fontsize=6.3, color=OPEN_C, ha="center")
    ax2.text(4.3, -10.5, "abstract enums /\nepistemic-bar", fontsize=6.3, color=CLOSED_C, ha="center")
    ax2.set_ylim(-13, 23)
    for ax in (ax1, ax2):
        ax.tick_params(labelsize=7.5); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(pad=0.4)
    fig.savefig(OUT / "aggregate.pdf"); fig.savefig(OUT / "aggregate.png", dpi=200)
    print("wrote", OUT / "aggregate.pdf")


make_aggregate_figure()
