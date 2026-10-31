import pandas as pd, numpy as np
import statsmodels.api as sm
df = pd.read_csv("data.csv")
print(df.isna().sum().sum(), df.shape)
y = df["export_growth_2023"]
lo, hi = y.quantile([0.01, 0.99])
d = df[(y >= lo) & (y <= hi)].copy()
d["region"] = d["region"].astype("category")
d["product_group"] = d["product_group"].astype("category")
def fit(f, data):
    m = sm.formula.ols(f, data=data).fit(cov_type="HC1")
    return round(m.params["supplier_diversity"],3), round(m.bse["supplier_diversity"],3), round(m.pvalues["supplier_diversity"],4)
base = "export_growth_2023 ~ supplier_diversity + log_sales_2020 + years_exporting_2020"
print("base", fit(base, d))
print("full pre-period controls", fit(base + " + export_growth_2020 + inventory_days_2020 + foreign_owned + share_imported_inputs_2020 + port_distance_km + certified_iso + debt_ratio_2020 + listed + C(region) + C(product_group)", d))
print("untrimmed base", fit(base, df))
print("export_growth_2020 only", fit("export_growth_2023 ~ supplier_diversity + export_growth_2020", d))
print("no controls", fit("export_growth_2023 ~ supplier_diversity", d))
print(d[["supplier_diversity","export_growth_2020","log_sales_2020","years_exporting_2020","inventory_days_2020","share_imported_inputs_2020","debt_ratio_2020"]].corr().round(3))
