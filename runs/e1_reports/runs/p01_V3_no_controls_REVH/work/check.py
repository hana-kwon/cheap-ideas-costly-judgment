import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_csv("data.csv")
print(df.shape)
print(df.describe(include="all").T.to_string())
print(df.isna().sum().to_string())

def fit(d, cols, label):
    d = d.dropna(subset=["productivity_2023", "training_hours"] + cols)
    X = d[["training_hours"] + cols].astype(float)
    if "sector" in cols or "region" in cols:
        pass
    X = sm.add_constant(X)
    r = sm.OLS(d["productivity_2023"].astype(float), X).fit(cov_type="HC1")
    print(label, "n=", len(d), "coef=", round(r.params["training_hours"], 4),
          "se=", round(r.bse["training_hours"], 4), "p=", round(r.pvalues["training_hours"], 4))

y = df["productivity_2023"]
lo, hi = y.quantile([0.01, 0.99])
t = df[(y >= lo) & (y <= hi)].copy()

# dummies
for c in ["region", "sector"]:
    if c in t.columns:
        dd = pd.get_dummies(t[c], prefix=c, drop_first=True).astype(float)
        t = pd.concat([t, dd], axis=1)
dummy_cols = [c for c in t.columns if c.startswith("region_") or c.startswith("sector_")]

fit(t, [], "baseline trimmed")
fit(df, [], "baseline untrimmed")
num = ["log_employees_2020", "firm_age_2020", "productivity_2020", "export_share_2020",
       "foreign_owned", "family_owned", "rd_intensity_2020", "union_share_2020", "credit_score_2020", "listed"]
num = [c for c in num if c in t.columns]
fit(t, num, "with pre-period controls")
fit(t, num + dummy_cols, "with controls+region/sector")
fit(t, ["productivity_2020"], "with lagged productivity")
fit(t, ["log_employees_2020"], "with size")
print(t[["training_hours", "log_employees_2020", "productivity_2020", "productivity_2023"]].corr().to_string())
