import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_csv("data.csv")
print(df.shape)
print(df.describe().T.to_string())
print(df.isna().sum().to_string())

def fit(cols, trim=True, d=df):
    d = d.dropna(subset=cols + ["export_growth_2023"]).copy()
    if trim:
        y = d["export_growth_2023"]
        lo, hi = y.quantile([0.01, 0.99])
        d = d[(y >= lo) & (y <= hi)]
    X = sm.add_constant(d[cols].astype(float))
    r = sm.OLS(d["export_growth_2023"].astype(float), X).fit(cov_type="HC1")
    return len(d), r.params["supplier_diversity"], r.bse["supplier_diversity"], r.pvalues["supplier_diversity"]

base = ["supplier_diversity", "log_sales_2020", "years_exporting_2020", "export_growth_2020"]
print("report spec (with buyer_rating):", fit(base + ["buyer_rating_2023"]))
print("without buyer_rating:", fit(base))
print("no trim, without buyer_rating:", fit(base, trim=False))
print("corr supplier_diversity vs buyer_rating:", df[["supplier_diversity", "buyer_rating_2023"]].corr().iloc[0, 1])
print("corr buyer_rating vs outcome:", df[["buyer_rating_2023", "export_growth_2023"]].corr().iloc[0, 1])
print("simple bivariate:", fit(["supplier_diversity"]))
