import pandas as pd, numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

df0 = pd.read_csv("data.csv")
print(df0.describe().T.to_string())
print(df0['region'].value_counts())
print("remote_share<0:", (df0.remote_share < 0).sum(), " >1:", (df0.remote_share > 1).sum())
print("missing:", df0.isna().sum()[df0.isna().sum() > 0].to_dict())
print("dup ids:", df0.firm_id.duplicated().sum())

def run(d, controls, label, trim=True):
    d = d.dropna(subset=['patents_per_100_eng_2023', 'remote_share'] + controls).copy()
    if trim:
        y = d.patents_per_100_eng_2023
        lo, hi = y.quantile([0.01, 0.99])
        d = d[(y >= lo) & (y <= hi)]
    X = sm.add_constant(d[['remote_share'] + controls].astype(float))
    f = sm.OLS(d.patents_per_100_eng_2023.astype(float), X).fit(cov_type='HC1')
    print(f"{label:45s} n={len(d):5d} b={f.params['remote_share']:.3f} se={f.bse['remote_share']:.3f} p={f.pvalues['remote_share']:.4f}")

C = ['log_engineers_2020', 'firm_age_2020', 'patents_per_100_eng_2020']
run(df0, C, "full sample, confounders")
run(df0, [], "full sample, no controls")
run(df0[df0.region == 'central'], C, "central, confounders (report)")
run(df0[df0.region == 'central'], [], "central, no controls")
run(df0[df0.region == 'north'], C, "north, confounders")
run(df0[df0.region == 'south'], C, "south, confounders")
run(df0, C + ['collab_index_2023', 'listed', 'vc_backed', 'founder_ceo', 'cloud_spend_2020', 'hq_in_hub_city', 'share_phd_2020', 'gross_margin_2020'], "full, all controls")
run(df0, C, "full, confounders, no trim", trim=False)
for r in ['north', 'central', 'south']:
    d = df0[df0.region == r]
    print(r, d.remote_share.describe()[['mean', 'std', 'min', 'max']].round(3).to_dict(),
          d.patents_per_100_eng_2023.describe()[['mean', 'std']].round(2).to_dict())
# region interaction test
f = smf.ols('patents_per_100_eng_2023 ~ remote_share*C(region) + ' + '+'.join(C), data=df0).fit(cov_type='HC1')
print(f.summary().tables[1])
