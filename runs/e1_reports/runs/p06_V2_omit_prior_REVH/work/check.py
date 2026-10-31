import pandas as pd, numpy as np
import statsmodels.api as sm
df = pd.read_csv("data.csv")
y = df["export_growth_2023"]
lo, hi = y.quantile([0.01, 0.99])
t = df[(y >= lo) & (y <= hi)].copy()

def run(d, cols, label):
    X = sm.add_constant(d[['supplier_diversity'] + cols].astype(float))
    f = sm.OLS(d["export_growth_2023"].values, X.values).fit(cov_type="HC1")
    ci = f.conf_int()[1]
    print(f"{label:45s} n={len(d)} b={f.params[1]:.3f} se={f.bse[1]:.3f} p={f.pvalues[1]:.4f} CI=[{ci[0]:.3f},{ci[1]:.3f}]")

base = ['log_sales_2020', 'years_exporting_2020']
run(df, [], "raw, no controls, untrimmed")
run(df, base, "reported spec, untrimmed")
run(t, base, "reported spec (trimmed) [replicate]")
run(t, [], "trimmed, no controls")
full = base + ['export_growth_2020', 'buyer_rating_2023', 'listed', 'foreign_owned',
               'inventory_days_2020', 'share_imported_inputs_2020', 'port_distance_km',
               'certified_iso', 'debt_ratio_2020']
d2 = pd.concat([t, pd.get_dummies(t[['region', 'product_group']], drop_first=True).astype(float)], axis=1)
run(d2, full + ['region_north' if 'region_north' in d2 else 'region_south'] + [c for c in d2.columns if c.startswith('product_group_')], "trimmed, full pre-period controls")
# outcome in logs-ish / growth scale check
print("outcome sd:", y.std(), "supplier_diversity sd:", df.supplier_diversity.std())
# corr of diversity with controls
print(df[['supplier_diversity'] + full].corr()['supplier_diversity'].round(3).to_string())
