import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_csv("<run_root>/e1R_261029/runs/p06_V3_no_controls_REVH/work/data.csv")
print(df.shape)
print(df.isna().sum())
print(df.describe().T)

y = df["export_growth_2023"]
lo, hi = y.quantile([0.01, 0.99])
d = df[(y >= lo) & (y <= hi)].copy()

def fit(cols, data):
    d2 = data.dropna(subset=cols + ["export_growth_2023"])
    X = d2[cols].astype(float).copy()
    if "region" in cols or "product_group" in cols:
        pass
    X = sm.add_constant(X)
    r = sm.OLS(d2["export_growth_2023"].astype(float), X).fit(cov_type="HC1")
    return len(d2), r.params["supplier_diversity"], r.bse["supplier_diversity"], r.pvalues["supplier_diversity"]

print("naive:", fit(["supplier_diversity"], d))

num_ctrl = ["log_sales_2020", "years_exporting_2020", "export_growth_2020", "inventory_days_2020",
            "foreign_owned", "share_imported_inputs_2020", "port_distance_km", "certified_iso",
            "debt_ratio_2020", "listed"]
for c in num_ctrl:
    if c in d.columns:
        print(c, "corr w/ treatment:", round(d[[c, "supplier_diversity"]].astype(float).corr().iloc[0, 1], 3),
              "corr w/ outcome:", round(d[[c, "export_growth_2023"]].astype(float).corr().iloc[0, 1], 3))
print("full controls:", fit(["supplier_diversity"] + [c for c in num_ctrl if c in d.columns], d))
