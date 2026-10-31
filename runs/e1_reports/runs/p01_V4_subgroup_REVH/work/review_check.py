import pandas as pd, numpy as np
import statsmodels.api as sm
df0 = pd.read_csv("data.csv")
def run(df, cols, trim=True, label=""):
    d = df.copy()
    if trim:
        y = d["productivity_2023"]; lo, hi = y.quantile([0.01, 0.99]); d = d[(y>=lo)&(y<=hi)]
    X = sm.add_constant(d[['training_hours']+cols].astype(float))
    f = sm.OLS(d["productivity_2023"].values, X.values).fit(cov_type="HC1")
    ci = f.conf_int()[1]
    print(f"{label:40s} n={len(d)} b={f.params[1]:.3f} se={f.bse[1]:.3f} p={f.pvalues[1]:.4f} CI=[{ci[0]:.2f},{ci[1]:.2f}]")
base=['log_employees_2020','firm_age_2020','productivity_2020']
run(df0[df0.region=='north'], base, True, "north, base, trim")
run(df0[df0.region=='north'], base, False, "north, base, no trim")
run(df0, base, True, "all, base, trim")
run(df0, base, False, "all, base, no trim")
run(df0, base+['mgmt_rating_2023'], False, "all, +mgmt")
run(df0, base+['listed','sector','export_share_2020','foreign_owned','family_owned','rd_intensity_2020','union_share_2020','credit_score_2020'], False, "all, full controls")
for r in ['north','central','south']:
    run(df0[df0.region==r], base, False, f"region {r}")
run(df0, [], False, "all, no controls")
print(df0[['training_hours','productivity_2023']].corr())
print(df0.groupby('region').training_hours.mean())
