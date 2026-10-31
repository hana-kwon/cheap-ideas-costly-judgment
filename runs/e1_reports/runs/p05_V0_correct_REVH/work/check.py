import pandas as pd, numpy as np
import statsmodels.api as sm
df = pd.read_csv("data.csv")
print(df.describe().T.to_string())
print("remote_share<0:", (df.remote_share<0).sum(), " >1:", (df.remote_share>1).sum())
print("missing:", df.isna().sum().to_dict())
y = df["patents_per_100_eng_2023"]
lo, hi = y.quantile([0.01, 0.99])
d = df[(y >= lo) & (y <= hi)].dropna(subset=['remote_share','log_engineers_2020','firm_age_2020','patents_per_100_eng_2020'])
X = sm.add_constant(d[['remote_share','log_engineers_2020','firm_age_2020','patents_per_100_eng_2020']].astype(float))
f = sm.OLS(d["patents_per_100_eng_2023"].values, X.values).fit(cov_type="HC1")
print("orig n", len(d), f.params[1], f.bse[1], f.pvalues[1], f.conf_int()[1])
# full controls incl pre-period firm characteristics
cols = ['remote_share','log_engineers_2020','firm_age_2020','patents_per_100_eng_2020','vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020','listed']
d2 = df.dropna(subset=cols+['patents_per_100_eng_2023'])
X2 = sm.add_constant(d2[cols].astype(float))
f2 = sm.OLS(d2["patents_per_100_eng_2023"].values, X2.values).fit(cov_type="HC1")
print("full controls n", len(d2), f2.params[1], f2.bse[1], f2.pvalues[1], f2.conf_int()[1])
# no trim
X3 = sm.add_constant(df[['remote_share','log_engineers_2020','firm_age_2020','patents_per_100_eng_2020']].astype(float))
f3 = sm.OLS(df["patents_per_100_eng_2023"].values, X3.values).fit(cov_type="HC1")
print("no trim", f3.params[1], f3.bse[1], f3.pvalues[1], f3.conf_int()[1])
