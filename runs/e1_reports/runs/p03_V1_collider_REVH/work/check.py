import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_csv("<run_root>/e1R_261029/runs/p03_V1_collider_REVH/work/data.csv")
print(df.shape)
print(df.describe().T.to_string())
print(df.isna().sum().to_string())

y = df["export_growth_2023"]
lo, hi = y.quantile([0.01, 0.99])
d = df[(y >= lo) & (y <= hi)].dropna(subset=["supplier_diversity", "log_sales_2020", "years_exporting_2020", "export_growth_2020", "buyer_rating_2023", "export_growth_2023"])

def fit(cols, label, data=d):
    X = sm.add_constant(data[["supplier_diversity"] + cols].astype(float))
    r = sm.OLS(data["export_growth_2023"].astype(float), X).fit(cov_type="HC1")
    print(f"{label}: b={r.params['supplier_diversity']:.4f} se={r.bse['supplier_diversity']:.4f} p={r.pvalues['supplier_diversity']:.4g} n={len(data)}")

fit([], "no controls")
fit(["log_sales_2020", "years_exporting_2020", "export_growth_2020"], "pre-period controls only (report minus buyer_rating)")
fit(["log_sales_2020", "years_exporting_2020", "export_growth_2020", "buyer_rating_2023"], "report spec")
fit(["log_sales_2020", "years_exporting_2020", "export_growth_2020", "inventory_days_2020", "foreign_owned", "share_imported_inputs_2020", "port_distance_km", "certified_iso", "debt_ratio_2020", "listed"], "all pre-period controls")

# does buyer_rating depend on supplier_diversity?
X = sm.add_constant(d[["supplier_diversity", "log_sales_2020", "years_exporting_2020", "export_growth_2020"]].astype(float))
r = sm.OLS(d["buyer_rating_2023"].astype(float), X).fit()
print("buyer_rating ~ supplier_diversity: b=%.4f p=%.4g R2=%.3f" % (r.params["supplier_diversity"], r.pvalues["supplier_diversity"], r.rsquared))
