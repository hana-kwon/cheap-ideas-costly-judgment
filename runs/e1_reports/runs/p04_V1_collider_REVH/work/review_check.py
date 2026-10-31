import pandas as pd, numpy as np
import statsmodels.api as sm
df = pd.read_csv("data.csv")
print(df.isna().sum().sum(), "missing")
y = df["productivity_2023"]
lo, hi = y.quantile([0.01, 0.99])
d = df[(y>=lo)&(y<=hi)].dropna(subset=['training_hours','log_employees_2020','firm_age_2020','productivity_2020','mgmt_rating_2023'])
def fit(cols, data):
    X = sm.add_constant(data[cols].astype(float))
    r = sm.OLS(data["productivity_2023"].astype(float), X).fit(cov_type="HC1")
    return round(r.params['training_hours'],4), round(r.bse['training_hours'],4), round(r.pvalues['training_hours'],4), len(data)
print("bivariate untrimmed", fit(['training_hours'], df))
print("bivariate trimmed", fit(['training_hours'], d))
print("ctrl size/age/pre", fit(['training_hours','log_employees_2020','firm_age_2020','productivity_2020'], d))
print("with mgmt", fit(['training_hours','log_employees_2020','firm_age_2020','productivity_2020','mgmt_rating_2023'], d))
print("corr training vs mgmt", np.corrcoef(d.training_hours, d.mgmt_rating_2023)[0,1])
print("corr training vs prod2023", np.corrcoef(d.training_hours, d.productivity_2023)[0,1])
print("corr mgmt vs prod2023", np.corrcoef(d.mgmt_rating_2023, d.productivity_2023)[0,1])
print("corr training vs prod2020", np.corrcoef(d.training_hours, d.productivity_2020)[0,1])
