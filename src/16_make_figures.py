# ============================================================
# START DATE   : 2026-10-30
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~10 s
# DESCRIPTION  : The two proposal figures. Figure 1: effective number of independent reviewers (panel a) and
#                planted ledger errors that survive each evaluation structure (panel b). Figure 2: report-task
#                approvals of method-flawed reports (panel a) and rejections of correct reports (panel b).
#                Each figure is written with the data it plots (figure_N_data.csv).
# INPUT FILES  : <e1_analysis.json> (src/13), <e2e3_analysis.json> (src/15)
# OUTPUT FILES : <out>/figure_1.{pdf,png}, figure_1_data.csv, figure_2.{pdf,png}, figure_2_data.csv
# USAGE        : python src/16_make_figures.py <e1_analysis.json> <e2e3_analysis.json> <out dir>
# ============================================================
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D

if len(sys.argv) != 4:
    sys.exit("usage: python src/16_make_figures.py <e1_analysis.json> <e2e3_analysis.json> <out dir>")
E1 = json.load(open(sys.argv[1]))
E23 = json.load(open(sys.argv[2]))
HERE = Path(sys.argv[3])
HERE.mkdir(parents=True, exist_ok=True)


def pick_font():
    """The proposal figures use Calibri. Where it is not installed, Carlito (metric-compatible) or the
    matplotlib default is used; only the typeface changes, not the numbers."""
    for name in ("Calibri", "Carlito"):
        try:
            font_manager.findfont(name, fallback_to_default=False)
            return name
        except ValueError:
            continue
    return "DejaVu Sans"


FONT = pick_font()
plt.rcParams.update({
    "font.family": FONT, "font.size": 9.5, "axes.labelsize": 9.5, "xtick.labelsize": 9,
    "ytick.labelsize": 9, "legend.fontsize": 9, "axes.linewidth": 0.6,
    "axes.spines.top": False, "axes.spines.right": False, "text.color": "black",
    "axes.labelcolor": "black", "pdf.fonttype": 42, "ps.fonttype": 42,
    "savefig.facecolor": "white", "figure.facecolor": "white",
})
INK, GRAY, GRID = "#111111", "#707070", "#e5e5e5"


def save(fig, stem, rows, header):
    fig.savefig(HERE / f"{stem}.pdf")
    fig.savefig(HERE / f"{stem}.png", dpi=600)
    with open(HERE / f"{stem}_data.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


c1, x1 = E1["confirmatory"], E1["exploratory_L"]
c23 = E23["confirmatory"]

# ★ CORE LOGIC: Figure 1. Panel (a) n_eff = 3 / (1 + 2 rho) for three reviewers; 3 means independent
# judgments, 1 means three copies of one judgment. Panel (b) share of seeded ledger errors still wrong
# in the final ledger, by evaluation structure.
neff = [  # label, ledger, report (None = not run)
    ("Same model,\nsame instructions", c1["H2L_dependence_REV123_miss"]["n_eff"],
     c1["H2R_dependence_REV123_approve_flawed"]["n_eff"]),
    ("Same model,\ndifferent roles", c23["H5L_role_vs_same_rho_miss"]["n_eff_role"],
     c23["H5R_role_vs_same_rho_approve_flawed"]["n_eff_role"]),
    ("Two models", x1["mixed_dependence_REV1_REV2_REVH"]["n_eff"], None),
]
m = x1["means_seeded"]
passed = [
    ("One review", m["REV1"]["pass_"]),
    ("Three reviews,\nany one flags", 1 - x1["panel_detect_any_majority_all"]["any"]),
    ("One review with\nfield checklist", m["TGT"]["pass_"]),
    ("Independent\nreproduction\nand comparison", m["REPRO"]["pass_"]),
]

fig, (a, b) = plt.subplots(1, 2, figsize=(6.5, 2.7), gridspec_kw={"width_ratios": [1, 1.05], "wspace": 0.75})
ys = list(range(len(neff)))[::-1]
for y, (lab, led, rep) in zip(ys, neff):
    a.plot(led, y + 0.13, "o", color=INK, markersize=6, zorder=3)
    if rep is not None:
        a.plot(rep, y - 0.13, "s", color=INK, markerfacecolor="white", markersize=6, markeredgewidth=1, zorder=3)
a.axvline(3, color=GRAY, linewidth=0.7, linestyle=(0, (3, 2)))
a.text(2.96, ys[0] + 0.45, "Independent", ha="right", va="center", fontsize=8.5, color=GRAY)
a.set_yticks(ys)
a.set_yticklabels([n[0] for n in neff])
a.set_xlim(0.9, 3.1)
a.set_ylim(-0.6, len(neff) - 0.3)
a.set_xticks([1, 1.5, 2, 2.5, 3])
a.set_xlabel("Effective number of independent\nreviewers among three")
a.grid(axis="x", color=GRID, linewidth=0.45)
a.text(-0.02, 1.04, "(a)", transform=a.transAxes, ha="right", fontsize=9.5)
a.legend(handles=[Line2D([], [], marker="o", color=INK, lw=0, markersize=5.5, label="Ledgers"),
                  Line2D([], [], marker="s", color=INK, markerfacecolor="white", lw=0, markersize=5.5,
                         label="Reports")], loc="lower right", frameon=False, handletextpad=0.3,
         borderaxespad=0.1)

yb = list(range(len(passed)))[::-1]
for y, (lab, v) in zip(yb, passed):
    b.barh(y, 100 * v, height=0.55, color=INK if y == yb[-1] else GRAY, zorder=2)
    b.text(100 * v + 0.12, y, f"{100 * v:.1f}" if v >= 0.01 else f"{100 * v:.2f}", va="center", fontsize=8.5)
b.set_yticks(yb)
b.set_yticklabels([p[0] for p in passed])
b.set_xlim(0, 6.2)
b.set_xlabel("Seeded errors left in final ledger (%)")
b.grid(axis="x", color=GRID, linewidth=0.45)
b.text(-0.02, 1.04, "(b)", transform=b.transAxes, ha="right", fontsize=9.5)
fig.subplots_adjust(left=0.17, right=0.98, bottom=0.25, top=0.92)
save(fig, "figure_1",
     [("a", n[0].replace("\n", " "), "ledger", round(n[1], 4)) for n in neff]
     + [("a", n[0].replace("\n", " "), "report", round(n[2], 4)) for n in neff if n[2] is not None]
     + [("b", p[0].replace("\n", " "), "ledger", round(p[1], 4)) for p in passed],
     ["panel", "structure", "task", "value"])
plt.close(fig)

# ★ CORE LOGIC: Figure 2, report task. Panel (a) approvals of the 12 flawed reports whose conclusion is
# still right (method errors only). Panel (b) rejections of the 6 correct reports (the cost side).
# "Review" is the mean of three same-model reviewers; reproduction compares conclusions only.
fa, fr = E1["exploratory_R"]["false_approval_flawed_right_conclusion"], E1["exploratory_R"]["false_rejection_correct"]
e2a = E23["exploratory"]["R_false_approval_flawed_right_concl"]
rev_rej = sum(fr[k] for k in ("REV1", "REV2", "REV3")) / 3
arms = [  # label, approve flawed (right conclusion), reject correct
    ("Review", e2a["REV"], rev_rej),
    ("Review by smaller model", fa["REVH"], fr["REVH"]),
    ("Review with checklist", fa["TGT"], fr["TGT"]),
    ("Own analysis, then review", e2a["PTR"], E23["exploratory"]["R_false_rejection_correct"]["PTR"]),
    ("Reproduce, compare conclusion", fa["REPRO"], fr["REPRO"]),
    ("Fixed rule list, no model", fa["CHK"], fr["CHK"]),
]
fig, (a, b) = plt.subplots(1, 2, figsize=(6.5, 2.6), sharey=True, gridspec_kw={"wspace": 0.12})
yy = list(range(len(arms)))[::-1]
for ax, j, xl in ((a, 1, "Method-flawed reports approved (%)"), (b, 2, "Correct reports rejected (%)")):
    for y, arm in zip(yy, arms):
        ax.barh(y, 100 * arm[j], height=0.55, color=GRAY, zorder=2)
        ax.text(100 * arm[j] + 2, y, f"{100 * arm[j]:.0f}", va="center", fontsize=8.5)
    ax.set_xlim(0, 115)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel(xl)
    ax.grid(axis="x", color=GRID, linewidth=0.45)
a.set_yticks(yy)
a.set_yticklabels([x[0] for x in arms])
a.text(-0.02, 1.04, "(a)", transform=a.transAxes, ha="right", fontsize=9.5)
b.text(-0.02, 1.04, "(b)", transform=b.transAxes, ha="right", fontsize=9.5)
fig.subplots_adjust(left=0.27, right=0.98, bottom=0.18, top=0.92)
save(fig, "figure_2", [(x[0], round(x[1], 4), round(x[2], 4)) for x in arms],
     ["structure", "approve_flawed_right_conclusion", "reject_correct"])
plt.close(fig)
print("matplotlib", matplotlib.__version__, "python", sys.version.split()[0], "font", FONT)
