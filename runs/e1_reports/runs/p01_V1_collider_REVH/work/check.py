import pandas as pd, numpy as np
import statsmodels.api as sm
df = pd.read_csv("data.csv")
print(df.shape)
print(df.describe().T.to_string())
print(df.isna().sum().to_string())
d = df.dropna(subset=['productivity_2023','training_hours','log_employees_2020','firm_age_2020','productivity_2020','mgmt_rating_2023']).copy()
y = d["productivity_2023"]
lo, hi = y.quantile([0.01, 0.99])
d = d[(y >= lo) & (y <= hi)]
def fit(cols):
    X = sm.add_constant(d[cols].astype(float))
    r = sm.OLS(d["productivity_2023"].values, X.values).fit(cov_type="HC1")
    print(cols, "n=",len(d), "coef=%.3f se=%.3f p=%.4f" % (r.params[1], r.bse[1], r.pvalues[1]))
fit(['training_hours'])
fit(['training_hours','log_employees_2020','firm_age_2020','productivity_2020'])
fit(['training_hours','log_employees_2020','firm_age_2020','productivity_2020','mgmt_rating_2023'])
print(np.corrcoef(d['training_hours'], d['mgmt_rating_2023'])[0,1])
print(np.corrcoef(d['mgmt_rating_2023'], d['productivity_2023'])[0,1])
print(np.corrcoef(d['training_hours'], d['productivity_2023'])[0,1])
