"""Concept figure: Hart's 'no vehicles in the park' as the S-3 statute.

One statute, three bindings of 'vehicle', three famous instances. Numbers in
the caption come from eval/expC/run_park.py. Run:
    .venv/bin/python paper/figures/make_concept_figure.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

OUT = Path(__file__).resolve().parent
CLOSED_C, OPEN_C, PROG_C = "#C44E52", "#4C72B0", "#222222"
OK, BAD = "#2E7D32", "#C62828"

fig, ax = plt.subplots(figsize=(3.5, 3.9))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")


def box(x, y, w, h, text, edge, title=None, fs=5.6):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.012", fc="white",
                                ec=edge, lw=1.1))
    ty = y + h / 2 - 0.014
    if title:
        ax.text(x, ty, title, ha="center", va="top", fontsize=fs + 0.9,
                fontweight="bold", color=edge)
        ty -= 0.046
    ax.text(x, ty, text, ha="center", va="top", fontsize=fs,
            color="#222222", linespacing=1.45)


# statute (the formal skeleton — identical across bindings)
box(0.5, 0.905, 0.95, 0.155,
    "S0  entry with one's effects: permitted\n"
    "S1  if VEHICLE: forbidden            (S1 beats S0)\n"
    "S2  if EMERGENCY: obligatory      (S2 beats S1)",
    "#555555", title="PARK ORDINANCE — formal skeleton (engine, exact)",
    fs=5.8)

ax.text(0.5, 0.800, 'what binds "VEHICLE" to the case?', ha="center",
        fontsize=6.0, style="italic", color="#555555")
for x0 in (0.17, 0.50, 0.83):
    ax.annotate("", xy=(x0, 0.715), xytext=(0.50, 0.788),
                arrowprops=dict(arrowstyle="->", lw=0.8, color="#777777"))

box(0.17, 0.625, 0.30, 0.175,
    "id $\\in$ {car, truck,\nmotorcycle, bicycle}\ncompile-time lookup",
    PROG_C, title="program")
box(0.50, 0.625, 0.30, 0.175,
    '“a car; a truck; a\nmotorcycle; a bicycle”\nLLM reads the list',
    CLOSED_C, title="closed + LLM")
box(0.83, 0.625, 0.31, 0.175,
    '“a conveyance bringing\ntraffic hazard into the park;\nwalking aids excluded”',
    OPEN_C, title="open + LLM")

# instance matrix
rows = [
    ("car (1958)", "forbidden",
     [("forbidden", True), ("forbidden", True), ("forbidden", True)]),
    ("e-scooter (2026)", "forbidden",
     [("permitted", False), ("permitted", False), ("forbidden", True)]),
    ("powered wheelchair", "permitted",
     [("permitted*", True), ("permitted*", True), ("permitted", True)]),
]
name_x, gold_x = 0.02, 0.345
cols_x = [0.535, 0.715, 0.895]
y0, dy = 0.435, 0.078
ax.text(name_x, y0, "instance", fontsize=6.2, fontweight="bold", va="center")
ax.text(gold_x, y0, "gold", fontsize=6.2, fontweight="bold", va="center",
        ha="center")
for cx, lab, c in zip(cols_x, ["program", "closed", "open"],
                      [PROG_C, CLOSED_C, OPEN_C]):
    ax.text(cx, y0, lab, fontsize=6.2, fontweight="bold", color=c,
            va="center", ha="center")
ax.plot([0.015, 0.985], [y0 - 0.45 * dy] * 2, lw=0.5, color="#aaaaaa")
for i, (name, gold, preds) in enumerate(rows):
    y = y0 - (i + 1) * dy
    ax.text(name_x, y, name, fontsize=6.0, va="center")
    ax.text(gold_x, y, gold, fontsize=5.8, va="center", ha="center",
            style="italic")
    for cx, (pred, ok) in zip(cols_x, preds):
        ax.text(cx, y, ("✓ " if ok else "✗ ") + pred, fontsize=5.8,
                va="center", ha="center", color=OK if ok else BAD)
ax.text(name_x, y0 - 3.85 * dy,
        "* right by omission (not on the list), not by reason — only the\n"
        "   open intension states why a wheelchair is not a vehicle",
        fontsize=5.4, color="#555555", va="top", linespacing=1.4)

fig.tight_layout(pad=0.25)
fig.savefig(OUT / "concept_park.pdf")
fig.savefig(OUT / "concept_park.png", dpi=220)
print("wrote", OUT / "concept_park.pdf")
