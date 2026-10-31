import pandas as pd, numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

raw = pd.read_csv("data.csv")
print(raw.shape, raw.isna().sum().sum(), raw.firm_id.duplicated().sum())
print(raw.region.value_counts())
print(raw.describe().T[['mean','std','min','max']])

def run(df, controls, trim=True, label=""):
    d = df.dropna(subset=['export_growth_2023','supplier_diversity']+controls).copy()
    if trim:
        lo, hi = d.export_growth_2023.quantile([0.01, 0.99])
        d = d[(d.export_growth_2023>=lo)&(d.export_growth_2023<=hi)]
    X = sm.add_constant(d[['supplier_diversity']+controls].astype(float))
    f = sm.OLS(d.export_growth_2023.astype(float), X).fit(cov_type="HC1")
    print(f"{label:40s} n={len(d):5d} b={f.params['supplier_diversity']:.3f} se={f.bse['supplier_diversity']:.3f} p={f.pvalues['supplier_diversity']:.4f}")

base = ['log_sales_2020','years_exporting_2020','export_growth_2020']
run(raw, [], False, "none, full, untrimmed")
run(raw, base, False, "controls, full, untrimmed")
run(raw, base, True, "controls, full, trimmed")
for r in ['north','central','south']:
    run(raw[raw.region==r], base, True, f"controls, region={r}")
    run(raw[raw.region==r], [], True, f"none, region={r}")
# with extra pre-period covariates
extra = base + ['inventory_days_2020','foreign_owned','share_imported_inputs_2020','port_distance_km','certified_iso','debt_ratio_2020']
run(raw, extra, True, "all pre-period controls, full")
run(raw[raw.region=='north'], extra, True, "all pre-period controls, north")
# outcome in 2020 as placebo-like check
print(raw.groupby('region').export_growth_2023.describe())
