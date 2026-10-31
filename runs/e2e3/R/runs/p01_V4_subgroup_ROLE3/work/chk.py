import pandas as pd
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.region.value_counts())
f="productivity_2023 ~ training_hours + log_employees_2020 + firm_age_2020 + productivity_2020"
for r in ['north','central','south',None]:
    d = df if r is None else df[df.region==r]
    m = smf.ols(f,d).fit(cov_type="HC1")
    print(r,len(d),m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'])
m = smf.ols(f+"+C(region)",df).fit(cov_type="HC1")
print('fe',m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'])
m = smf.ols("productivity_2023 ~ training_hours*C(region)+log_employees_2020 + firm_age_2020 + productivity_2020",df).fit(cov_type="HC1")
print(m.summary().tables[1])
print(df.training_hours.describe())
