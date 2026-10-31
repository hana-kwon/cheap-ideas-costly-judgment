import pandas as pd, numpy as np
import statsmodels.api as sm
df = pd.read_csv("data.csv")
print(df.region.value_counts())
def fit(d, ctrl):
    y = d["export_growth_2023"]
    lo, hi = y.quantile([0.01, 0.99])
    d = d[(y >= lo) & (y <= hi)]
    X = sm.add_constant(d[['supplier_diversity'] + ctrl].astype(float))
    r = sm.OLS(d["export_growth_2023"].values, X.values).fit(cov_type="HC1")
    return len(d), round(r.params[1],3), round(r.bse[1],3), round(r.pvalues[1],4), np.round(r.conf_int()[1],3)
ctrl = ['log_sales_2020','years_exporting_2020','export_growth_2020']
print("north, report spec", fit(df[df.region=='north'], ctrl))
print("all, no ctrl", fit(df, []))
print("all, ctrl", fit(df, ctrl))
for r in ['north','central','south']:
    print(r, fit(df[df.region==r], ctrl))
