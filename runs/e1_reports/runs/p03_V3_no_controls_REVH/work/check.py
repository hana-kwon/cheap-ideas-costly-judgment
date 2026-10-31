import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_csv("<run_root>/e1R_261029/runs/p03_V3_no_controls_REVH/work/data.csv")
print(df.shape)
print(df.describe(include="all").T.to_string())
print(df.isna().sum().to_string())

d = df.dropna(subset=["export_growth_2023", "supplier_diversity"]).copy()
y = d["export_growth_2023"]
lo, hi = y.quantile([0.01, 0.99])
t = d[(y >= lo) & (y <= hi)].copy()

def fit(data, cols, label):
    X = sm.add_constant(data[["supplier_diversity"] + cols].astype(float))
    r = sm.OLS(data["export_growth_2023"].astype(float), X).fit(cov_type="HC1")
    print(label, "n=", len(data), "coef=%.4f se=%.4f p=%.4g" % (r.params["supplier_diversity"], r.bse["supplier_diversity"], r.pvalues["supplier_diversity"]))
    return r

fit(t, [], "raw trimmed")
fit(d, [], "raw untrimmed")
num = ["log_sales_2020", "years_exporting_2020", "export_growth_2020", "inventory_days_2020",
       "foreign_owned", "share_imported_inputs_2020", "port_distance_km", "certified_iso", "debt_ratio_2020", "listed"]
num = [c for c in num if c in d.columns]
for c in num:
    t[c] = pd.to_numeric(t[c], errors="coerce")
tt = t.dropna(subset=num)
fit(tt, [], "raw trimmed complete-case")
fit(tt, num, "with all pre-period controls")
for c in num:
    r = sm.OLS(t["supplier_diversity"].astype(float), sm.add_constant(t[[c]].astype(float)), missing="drop").fit()
    print("balance", c, "coef=%.4f p=%.4g" % (r.params[c], r.pvalues[c]))
