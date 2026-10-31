import pandas as pd
import numpy as np
import statsmodels.api as sm

df = pd.read_csv("data.csv")
print("N raw", len(df))
print(df.describe().T[['mean','std','min','max']])
print("NaN counts:\n", df.isna().sum()[df.isna().sum()>0])

y = df["patents_per_100_eng_2023"]
lo, hi = y.quantile([0.01, 0.99])
d = df[(y >= lo) & (y <= hi)].dropna(subset=['remote_share','log_engineers_2020','firm_age_2020','patents_per_100_eng_2020'])

def fit(cols, data, label):
    X = sm.add_constant(data[cols].astype(float))
    m = sm.OLS(data["patents_per_100_eng_2023"].astype(float), X).fit(cov_type="HC1")
    print(f"{label}: coef={m.params['remote_share']:.4f} se={m.bse['remote_share']:.4f} p={m.pvalues['remote_share']:.4g} n={len(data)}")

fit(['remote_share','log_engineers_2020','firm_age_2020'], d, "analyst spec")
fit(['remote_share'], d, "no controls")
fit(['remote_share','log_engineers_2020','firm_age_2020','patents_per_100_eng_2020'], d, "+ lagged outcome")
fit(['remote_share','log_engineers_2020','firm_age_2020','patents_per_100_eng_2020','vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020'], d, "+ all pre-period")

# balance: does remote_share correlate with 2020 outcome?
print("corr(remote_share, patents_2020)", d[['remote_share','patents_per_100_eng_2020']].corr().iloc[0,1])
print("corr(remote_share, patents_2023)", d[['remote_share','patents_per_100_eng_2023']].corr().iloc[0,1])
