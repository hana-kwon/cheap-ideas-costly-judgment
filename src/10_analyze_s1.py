# ============================================================
# START DATE   : 2026-10-28
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1 min
# DESCRIPTION  : Pre-specified analysis of the accountability experiment S1: paired packet-level contrasts H1-H3
#                (two-sided sign-flip permutation p, packet bootstrap 95 percent interval, Holm adjustment), then
#                the exploratory contrasts listed in the plan. Standard library only. Run once on the scores from
#                the parser fixed in the plan (src/08) and once on the content-based rescoring (src/09).
# INPUT FILES  : <scores>/packet_scores.csv
# OUTPUT FILES : <out>/analysis.json, printed table
# USAGE        : python src/10_analyze_s1.py <scores dir> <out dir>
# ============================================================
import csv
import json
import random
import sys
from pathlib import Path

B = 20000  # sign flips and bootstrap draws; fixed seeds so the numbers reproduce


def load(scores):
    rows = list(csv.DictReader(open(Path(scores) / "packet_scores.csv")))
    by = {}
    for r in rows:
        by.setdefault((r["tag"], r["fmt"]), {})[r["arm"]] = r
    return rows, by


# ★ KEY FUNCTION: paired difference over packets that have both arms and a defined outcome.
def paired(by, a1, a2, y, fmt=None):
    d = []
    for (tag, f), arms in by.items():
        if fmt and f != fmt:
            continue
        if a1 in arms and a2 in arms and arms[a1][y] != "" and arms[a2][y] != "":
            d.append(float(arms[a1][y]) - float(arms[a2][y]))
    if len(d) < 3:
        return dict(contrast=f"{a1}-{a2}", y=y, fmt=fmt or "all", n=len(d))
    m = sum(d) / len(d)
    rng = random.Random(f"{a1}{a2}{y}{fmt}")
    # two-sided sign-flip test of mean zero: under H0 each packet's difference is symmetric around 0
    hits = sum(abs(sum(x if rng.random() < 0.5 else -x for x in d)) >= abs(sum(d)) - 1e-12 for _ in range(B))
    boots = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(B))
    return dict(contrast=f"{a1}-{a2}", y=y, fmt=fmt or "all", n=len(d), mean_diff=round(m, 4),
                ci95=[round(boots[int(0.025 * B)], 4), round(boots[int(0.975 * B) - 1], 4)],
                p=round((hits + 1) / (B + 1), 5), share_positive=round(sum(x > 0 for x in d) / len(d), 3),
                share_zero=round(sum(x == 0 for x in d) / len(d), 3))


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj, run = [0.0] * len(ps), 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i]))
        adj[i] = round(run, 4)
    return adj


def main(scores, out):
    rows, by = load(scores)
    # ★ CORE LOGIC: the three confirmatory tests, exactly as fixed in the prereg.
    conf = [paired(by, "C", "B", "pass_through"),      # H1: owner approval lets more seeded errors through
            paired(by, "D", "B", "pass_unflagged"),    # H2: auto-confirmation lets more unflagged errors through
            paired(by, "B", "A", "final_error")]       # H3: checking a seeded draft ends worse than authoring
    adj = holm([c.get("p", 1.0) for c in conf])
    for c, h, a in zip(conf, ["H1", "H2", "H3"], adj):
        c["hyp"], c["p_holm"] = h, a
    expl = [paired(by, "B", "N", "pass_through"), paired(by, "C", "N", "pass_through"),
            paired(by, "D", "B", "pass_flagged"), paired(by, "D", "B", "pass_through"),
            paired(by, "C", "B", "harm"), paired(by, "D", "B", "harm")]
    for f in ("local", "standard"):
        expl += [paired(by, "C", "B", "pass_through", f), paired(by, "D", "B", "pass_unflagged", f)]
    means = {}
    for arm in ["A", "N", "B", "C", "D"]:
        rs = [r for r in rows if r["arm"] == arm]
        means[arm] = {y: round(sum(float(r[y]) for r in rs if r[y] != "") / max(1, sum(r[y] != "" for r in rs)), 4)
                      for y in ("pass_through", "pass_flagged", "pass_unflagged", "harm", "final_error")}
        means[arm]["n_packets"] = len(rs)
        means[arm]["bad_lines"] = sum(int(r["bad_lines"]) for r in rs)
        for q in ("ans_responsible", "ans_approver", "ans_author"):
            tally = {}
            for r in rs:
                tally[r[q] or "(none)"] = tally.get(r[q] or "(none)", 0) + 1
            means[arm][q] = tally
    res = dict(confirmatory=conf, exploratory=expl, arm_means=means)
    Path(out).mkdir(parents=True, exist_ok=True)
    Path(out, "analysis.json").write_text(json.dumps(res, indent=1))
    for c in conf:
        print(c)
    for arm, m in means.items():
        print(arm, {k: v for k, v in m.items() if not k.startswith("ans_")})
    return res


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
