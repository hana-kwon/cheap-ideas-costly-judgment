import pandas as pd, numpy as np
import statsmodels.api as sm
df = pd.read_csv("data.csv")
print(df.shape); print(df.isna().sum()); print(df.describe().T)
d = df.dropna(subset=['productivity_2023','training_hours','log_employees_2020','firm_age_2020','productivity_2020'])
y = d["productivity_2023"]; lo, hi = y.quantile([0.01,0.99]); d = d[(y>=lo)&(y<=hi)]
def fit(cols, data):
    X = sm.add_constant(data[cols].astype(float))
    r = sm.OLS(data["productivity_2023"].astype(float), X).fit(cov_type="HC1")
    return round(r.params["training_hours"],4), round(r.bse["training_hours"],4), round(r.pvalues["training_hours"],4), len(data)
base = ['training_hours','log_employees_2020','firm_age_2020','productivity_2020']
print("base", fit(base, d))
print("no pre outcome", fit(base[:-1], d))
extra = ['export_share_2020','foreign_owned','family_owned','rd_intensity_2020','union_share_2020','credit_score_2020','listed']
ex = [c for c in extra if c in d.columns]
print("full controls", fit(base+ex, d.dropna(subset=ex)))
print("with mgmt (post-period, bad control)", fit(base+['mgmt_rating_2023'], d.dropna(subset=['mgmt_rating_2023'])))
# untrimmed
d2 = df.dropna(subset=base+['productivity_2023'])
print("untrimmed", fit(base, d2))
