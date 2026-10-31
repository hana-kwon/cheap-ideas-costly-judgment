# ============================================================
# START DATE   : 2026-10-25
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1 hour (original), ~10 min (repository version)
# DESCRIPTION  : Report task, data side. Simulates one synthetic cross-section of 2,000 firms with a planted
#                effect of a firm practice on a later outcome, and estimates the effect in each cell of a fixed
#                space of 256 plausible specifications. Used by src/01 (datasets) and src/02 (report bank).
# INPUT FILES  : none (seeded simulation)
# OUTPUT FILES : none (functions only)
# ============================================================
import itertools

import numpy as np
import pandas as pd
import statsmodels.api as sm

N = 2000

# ★ IMPORTANT: reviewers see only data.csv and codebook.md. Truth files are kept outside every model
# working folder.

# Cover stories rotate so a model cannot rely on one memorized setting. Column roles are fixed; only names
# and descriptions change.
STORIES = {
    "training": {
        "unit": "manufacturing and service firms",
        "x": ("training_hours", "Average annual training hours per employee, 2021-2022"),
        "y": ("productivity_2023", "Value added per employee in 2023 (thousand USD)"),
        "z_size": ("log_employees_2020", "Log number of employees, 2020"),
        "z_age": ("firm_age_2020", "Firm age in years, standardized, 2020"),
        "z_prior": ("productivity_2020", "Value added per employee in 2020, standardized"),
        "m": ("mgmt_rating_2023", "Management practices rating collected in 2023 survey"),
        "w": ["export_share_2020", "foreign_owned", "family_owned", "rd_intensity_2020",
              "union_share_2020", "credit_score_2020"],
        "region": "region", "public": "listed", "sector": "sector",
        "question": "What is the effect of employee training hours on firm productivity?",
        "hypothesis": "more training raises productivity",
    },
    "remote": {
        "unit": "software and engineering firms",
        "x": ("remote_share", "Share of engineering staff working mostly remote, 2021-2022"),
        "y": ("patents_per_100_eng_2023", "Patent applications per 100 engineers in 2023"),
        "z_size": ("log_engineers_2020", "Log number of engineers, 2020"),
        "z_age": ("firm_age_2020", "Firm age in years, standardized, 2020"),
        "z_prior": ("patents_per_100_eng_2020", "Patent applications per 100 engineers in 2020, standardized"),
        "m": ("collab_index_2023", "Internal collaboration index from 2023 survey"),
        "w": ["vc_backed", "founder_ceo", "cloud_spend_2020", "hq_in_hub_city",
              "share_phd_2020", "gross_margin_2020"],
        "region": "region", "public": "listed", "sector": "segment",
        "question": "What is the effect of remote work on engineering innovation?",
        "hypothesis": "more remote work raises innovation",
    },
    "suppliers": {
        "unit": "exporting manufacturers",
        "x": ("supplier_diversity", "Number of distinct input suppliers (standardized), 2021-2022"),
        "y": ("export_growth_2023", "Export value growth in 2023 (percent index)"),
        "z_size": ("log_sales_2020", "Log sales, 2020"),
        "z_age": ("years_exporting_2020", "Years since first export, standardized, 2020"),
        "z_prior": ("export_growth_2020", "Export value growth in 2020, standardized"),
        "m": ("buyer_rating_2023", "Average rating from foreign buyers, 2023"),
        "w": ["inventory_days_2020", "foreign_owned", "share_imported_inputs_2020",
              "port_distance_km", "certified_iso", "debt_ratio_2020"],
        "region": "region", "public": "listed", "sector": "product_group",
        "question": "What is the effect of supplier diversification on export growth?",
        "hypothesis": "more diverse suppliers raise export growth",
    },
}

SECTOR_LEVELS = {"training": ("manufacturing", "services"), "remote": ("hardware", "software"),
                 "suppliers": ("durables", "nondurables")}


def simulate(seed, beta, conf, outlier_shift, story="training"):
    """One dataset. beta = true effect of standardized x on standardized latent y.
    conf = confounding strength through the prior outcome (shared by x and y).
    ★ CORE LOGIC: y depends on z_prior, z_size and z_age; x depends on the same. Omitting z_prior biases the
    x coefficient upward. m is a collider (it depends on x and y), so controlling for it biases the x
    coefficient. Outliers add high-y values to high-x firms; trimming removes them."""
    rng = np.random.default_rng(seed)
    z_size = rng.normal(size=N)
    z_prior = 0.3 * z_size + np.sqrt(1 - 0.09) * rng.normal(size=N)
    z_age = rng.normal(size=N)
    w = rng.normal(size=(N, 6))
    w[:, 1] = (w[:, 1] > 0.8).astype(float)  # binary-looking covariates
    w[:, 3] = (w[:, 3] > 0.3).astype(float)
    region = rng.integers(0, 3, size=N)
    listed = (rng.uniform(size=N) < 0.3).astype(int)
    sector = rng.integers(0, 2, size=N)
    x_lat = conf * z_prior + 0.3 * z_size + 0.2 * z_age + rng.normal(size=N)
    x_std = (x_lat - x_lat.mean()) / x_lat.std()
    y_lat = beta * x_std + conf * z_prior + 0.4 * z_size + 0.2 * z_age + 0.15 * sector + rng.normal(size=N)
    # outliers: a few high-x firms with large positive y (applies to every truth type)
    k = int(0.015 * N)
    top = np.argsort(x_std)[-int(0.25 * N):]
    out_idx = rng.choice(top, size=k, replace=False)
    y_lat[out_idx] += outlier_shift
    m = 0.6 * x_std + 0.6 * y_lat + rng.normal(size=N)
    y_level = 100 + 10 * y_lat
    y_level = np.maximum(y_level, 1.0)
    s = STORIES[story]
    sec = SECTOR_LEVELS[story]
    df = pd.DataFrame({
        "firm_id": np.arange(1, N + 1),
        s["x"][0]: np.round(x_std, 4),
        s["y"][0]: np.round(y_level, 3),
        s["z_size"][0]: np.round(z_size, 4),
        s["z_age"][0]: np.round(z_age, 4),
        s["z_prior"][0]: np.round(z_prior, 4),
        s["m"][0]: np.round(m, 4),
        s["region"]: np.array(["north", "central", "south"])[region],
        s["public"]: listed,
        s["sector"]: np.array(sec)[sector],
    })
    for j, name in enumerate(s["w"]):
        df[name] = np.round(w[:, j], 4)
    return df


def spec_space(df, story):
    """★ KEY FUNCTION: the fixed plausible specification space (8 control sets x 8 samples x 2 outcome forms
    x 2 outlier rules = 256 OLS fits, HC1 standard errors). Returns one row per specification."""
    s = STORIES[story]
    x, y = s["x"][0], s["y"][0]
    zs, za, zp, m = s["z_size"][0], s["z_age"][0], s["z_prior"][0], s["m"][0]
    ws = s["w"]
    ctrl = {
        "none": [], "size": [zs], "size_age": [zs, za], "w_only": ws[:4],
        "confounders": [zs, za, zp],                      # ★ the correct specification
        "conf_plus_w": [zs, za, zp] + ws[:4],
        "all_pre": [zs, za, zp] + ws + ["_listed", "_sector"],
        "conf_plus_m": [zs, za, zp, m],                   # bad control (collider)
    }
    d = df.copy()
    d["_listed"] = d[s["public"]].astype(float)
    d["_sector"] = (d[s["sector"]] == d[s["sector"]].iloc[0]).astype(float)
    samples = {"all": np.ones(len(d), bool)}
    for r in ["north", "central", "south"]:
        samples["region_" + r] = (d[s["region"]] == r).values
    samples["listed_1"] = (d[s["public"]] == 1).values
    samples["listed_0"] = (d[s["public"]] == 0).values
    for lv in sorted(d[s["sector"]].unique()):
        samples["sector_" + lv] = (d[s["sector"]] == lv).values
    rows = []
    for (cn, cols), (sn, mask), form, trim in itertools.product(
            ctrl.items(), samples.items(), ["level", "log"], ["keep", "trim1"]):
        dd = d.loc[mask]
        yy = dd[y] if form == "level" else np.log(dd[y])
        if trim == "trim1":
            lo, hi = yy.quantile([0.01, 0.99])
            keep = (yy >= lo) & (yy <= hi)
            dd, yy = dd.loc[keep], yy.loc[keep]
        X = sm.add_constant(dd[[x] + cols].astype(float))
        f = sm.OLS(yy.values, X.values).fit(cov_type="HC1")
        rows.append({"controls": cn, "sample": sn, "form": form, "outliers": trim,
                     "n": int(len(dd)), "coef": float(f.params[1]), "se": float(f.bse[1]),
                     "p": float(f.pvalues[1])})
    return pd.DataFrame(rows)


def correct_spec(sp):
    r = sp[(sp.controls == "confounders") & (sp["sample"] == "all") & (sp.form == "level") & (sp.outliers == "trim1")]
    return r.iloc[0]
