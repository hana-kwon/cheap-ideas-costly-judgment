import pandas as pd
import statsmodels.api as sm
df = pd.read_csv("data.csv")
y = df["export_growth_2023"]
lo, hi = y.quantile([0.01, 0.99])
t = df[(y >= lo) & (y <= hi)].copy()
base = ['log_sales_2020', 'years_exporting_2020']
def run(cols, label):
    X = sm.add_constant(t[['supplier_diversity'] + cols].astype(float))
    f = sm.OLS(t["export_growth_2023"].values, X.values).fit(cov_type="HC1")
    ci = f.conf_int()[1]
    print(f"{label:40s} b={f.params[1]:.3f} se={f.bse[1]:.3f} p={f.pvalues[1]:.4g} CI=[{ci[0]:.3f},{ci[1]:.3f}]")
run(base, "base")
run(base + ['export_growth_2020'], "+ export_growth_2020 (pre)")
run(base + ['buyer_rating_2023'], "+ buyer_rating_2023 (post, 2023)")
run(base + ['export_growth_2020', 'listed', 'foreign_owned', 'inventory_days_2020',
            'share_imported_inputs_2020', 'port_distance_km', 'certified_iso', 'debt_ratio_2020'], "+ all pre-period 2020 covariates")
