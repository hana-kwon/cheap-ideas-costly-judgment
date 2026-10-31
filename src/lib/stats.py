# ============================================================
# START DATE   : 2026-10-29
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~20 min (original), ~5 min (moved here)
# DESCRIPTION  : Test statistics fixed in the E1 and E2/E3 plans: two-sided sign-flip permutation test with a
#                bootstrap interval for paired differences, the dependence of three reviewers' misses (mean
#                pairwise correlation rho, effective number of independent reviewers 3 / (1 + 2 rho), one-sided
#                permutation test), the panel-swap test comparing two panels' dependence, and Holm adjustment.
#                Moved unchanged from the fixed analysis scripts so both analyses import one copy.
# INPUT FILES  : none
# OUTPUT FILES : none
# ============================================================
import itertools
import random

import numpy as np
import pandas as pd

B = 20000


def signflip(d, seed):
    """Two-sided sign-flip test of mean zero and bootstrap 95% CI, over independent units."""
    rng = random.Random(seed)
    d = [float(x) for x in d]
    m = sum(d) / len(d)
    hits = sum(abs(sum(x if rng.random() < 0.5 else -x for x in d)) >= abs(sum(d)) - 1e-12 for _ in range(B))
    boots = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(B))
    return dict(n=len(d), mean=round(m, 4), ci95=[round(boots[int(0.025 * B)], 4), round(boots[int(0.975 * B) - 1], 4)],
                p=round((hits + 1) / (B + 1), 5))


# ★ KEY FUNCTION: dependence among three reviewers' misses. rho = mean pairwise phi correlation of miss
# indicators; n_eff = 3 / (1 + 2 rho); ratio = P(all three miss) / product of single miss rates. The cluster
# bootstrap (descriptive CI only) resamples whole units; the test is a permutation test (below).
def dependence(df, cols, cluster, seed):
    def stats(d):
        M = d[cols].astype(float)
        rs = []
        for a, b in itertools.combinations(cols, 2):
            x, y = M[a], M[b]
            sx, sy = x.std(), y.std()
            if sx > 0 and sy > 0:
                rs.append(((x - x.mean()) * (y - y.mean())).mean() / (x.std(ddof=0) * y.std(ddof=0)))
        rho = sum(rs) / len(rs) if rs else float("nan")
        prod = 1.0
        for c in cols:
            prod *= M[c].mean()
        allm = M.all(axis=1).mean()
        return rho, (allm / prod if prod > 0 else float("nan")), allm, prod
    rho, ratio, allm, prod = stats(df)
    rng = random.Random(seed)
    units = df[cluster].unique().tolist()
    groups = {u: df[df[cluster] == u] for u in units}
    bs = []
    for _ in range(2000):
        d = pd.concat([groups[rng.choice(units)] for _ in units])
        r = stats(d)[0]
        if r == r:
            bs.append(r)
    bs.sort()
    # ★ IMPORTANT: the p-value comes from a permutation test, not the bootstrap (few clusters make the
    # bootstrap overconfident). Each reviewer's indicator vector is shuffled independently across items,
    # which keeps every reviewer's own rate and destroys only the co-occurrence of misses on the same item.
    vals = {c: df[c].astype(float).tolist() for c in cols}
    perm_ge = 0
    for _ in range(5000):
        d = pd.DataFrame({c: rng.sample(vals[c], len(vals[c])) for c in cols})
        r = stats(d)[0]
        if r == r and r >= rho - 1e-12:
            perm_ge += 1
    p_perm = (perm_ge + 1) / 5001
    return dict(rho=round(rho, 4), n_eff=round(3 / (1 + 2 * rho), 3) if rho == rho else None,
                ratio_all_vs_indep=round(ratio, 3) if ratio == ratio else None, p_all_miss=round(allm, 4),
                p_indep=round(prod, 5), rho_boot_ci95=[round(bs[int(0.025 * len(bs))], 4), round(bs[int(0.975 * len(bs)) - 1], 4)],
                p_one_sided=round(p_perm, 4), n_boot_valid=len(bs))


def holm(named):
    keys = list(named)
    ps = [named[k].get("p", named[k].get("p_one_sided", 1.0)) for k in keys]
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    run, adj = 0.0, {}
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i]))
        adj[keys[i]] = round(run, 4)
    return adj


def rho(M):
    rs = []
    for a, b in itertools.combinations(range(M.shape[1]), 2):
        x, y = M[:, a], M[:, b]
        sx, sy = x.std(), y.std()
        if sx > 0 and sy > 0:
            rs.append(((x - x.mean()) * (y - y.mean())).mean() / (sx * sy))
    return sum(rs) / len(rs) if rs else float("nan")


# ★ KEY FUNCTION: under H0 the two panels are exchangeable item by item, so swapping an item's triple of
# role-panel indicators with its triple of same-panel indicators leaves the distribution unchanged.
def panel_swap_test(A, B, seed, n=5000):
    A, B = np.asarray(A, float), np.asarray(B, float)
    obs = rho(A) - rho(B)
    rng = random.Random(seed)
    ge = 0
    for _ in range(n):
        sw = np.array([rng.random() < 0.5 for _ in range(len(A))])
        A2 = np.where(sw[:, None], B, A)
        B2 = np.where(sw[:, None], A, B)
        d = rho(A2) - rho(B2)
        if d == d and abs(d) >= abs(obs) - 1e-12:
            ge += 1
    return dict(rho_role=round(rho(A), 4), rho_same=round(rho(B), 4), diff=round(obs, 4),
                n_eff_role=round(3 / (1 + 2 * rho(A)), 3), n_eff_same=round(3 / (1 + 2 * rho(B)), 3),
                p=round((ge + 1) / (n + 1), 4), n_items=len(A))
