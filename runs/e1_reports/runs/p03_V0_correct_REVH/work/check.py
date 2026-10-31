import pandas as pd, numpy as np
import statsmodels.api as sm
df = pd.read_csv("data.csv")
print(df.shape)
print(df.isna().sum())
print(df.describe().T.to_string())
print(df.dtypes)
for c in ["region","listed","product_group"]:
    if c in df: print(df[c].value_counts(dropna=False))

def fit(d, cols, label):
    d = d.dropna(subset=["export_growth_2023"]+cols)
    y = d["export_growth_2023"]
    lo, hi = y.quantile([0.01,0.99])
    d = d[(y>=lo)&(y<=hi)]
    X = sm.add_constant(d[cols].astype(float))
    r = sm.OLS(d["export_growth_2023"].astype(float), X).fit(cov_type="HC1")
    print(label, "n=",len(d), "coef=%.3f se=%.3f p=%.4f" % (r.params["supplier_diversity"], r.bse["supplier_diversity"], r.pvalues["supplier_diversity"]))

base = ["supplier_diversity"]
conf = ["supplier_diversity","log_sales_2020","years_exporting_2020","export_growth_2020"]
fit(df, base, "bivariate")
fit(df, conf, "reported spec (dropna)")
full = conf + ["inventory_days_2020","foreign_owned","share_imported_inputs_2020","port_distance_km","certified_iso","debt_ratio_2020","listed"]
fit(df, full, "all pre-period")
# numeric check of collinearity of treatment with covariates
num = df.select_dtypes(include=float).columns.tolist()
print(df[num].corr()["supplier_diversity"].round(3).to_string())
