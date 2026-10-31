import pandas as pd
import numpy as np
import statsmodels.api as sm

df0 = pd.read_csv("data.csv")
print(df0.shape)
print(df0.isna().sum().to_dict())
print(df0['region'].value_counts().to_dict())
print(df0[['training_hours','productivity_2023']].describe().to_string())

def fit(d, controls, trim=True, label=""):
    d = d.dropna(subset=['productivity_2023','training_hours'] + controls).copy()
    if trim:
        y = d['productivity_2023']
        lo, hi = y.quantile([0.01, 0.99])
        d = d[(y >= lo) & (y <= hi)]
    X = sm.add_constant(d[['training_hours'] + controls].astype(float))
    r = sm.OLS(d['productivity_2023'].astype(float), X).fit(cov_type='HC1')
    ci = r.conf_int().loc['training_hours'].values
    print(f"{label:40s} n={len(d):5d} b={r.params['training_hours']:.4f} se={r.bse['training_hours']:.4f} p={r.pvalues['training_hours']:.4f} CI=[{ci[0]:.3f},{ci[1]:.3f}]")

ctrl = ['log_employees_2020', 'firm_age_2020', 'productivity_2020']
fit(df0, [], False, "full, no controls, no trim")
fit(df0, ctrl, True, "full, controls, trim")
fit(df0, ctrl, False, "full, controls, no trim")
for r in ['north','central','south']:
    fit(df0[df0.region==r], ctrl, True, f"region={r}, controls, trim")
    fit(df0[df0.region==r], ctrl, False, f"region={r}, controls, notrim")
fit(df0, ctrl+['mgmt_rating_2023','listed','export_share_2020','foreign_owned','family_owned','rd_intensity_2020','union_share_2020','credit_score_2020'], True, "full, all controls, trim")
