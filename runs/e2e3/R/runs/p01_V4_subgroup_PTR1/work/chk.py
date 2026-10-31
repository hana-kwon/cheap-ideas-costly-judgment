import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv("data.csv")
f="productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020"
for r in ['north','central','south']:
    m=smf.ols(f,d[d.region==r]).fit(cov_type="HC1");print(r,m.params['training_hours'],m.bse['training_hours'],len(d[d.region==r]))
m=smf.ols(f,d).fit(cov_type="HC1");print('all',m.params['training_hours'],m.bse['training_hours'])
