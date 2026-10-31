import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
m=smf.ols('productivity_2023~training_hours+I(training_hours**2)+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
m=smf.ols('productivity_2023~training_hours*C(sector)+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
print(d.training_hours.describe(), d.productivity_2023.describe())
for s,g in d.groupby('sector'):
    r=smf.ols('productivity_2023~training_hours+'+pre.replace('+C(sector)',''),g).fit(cov_type='HC1');print(s,r.params['training_hours'],r.bse['training_hours'])
for s,g in d.groupby('region'):
    r=smf.ols('productivity_2023~training_hours+'+pre.replace('+C(region)',''),g).fit(cov_type='HC1');print(s,r.params['training_hours'],r.bse['training_hours'])
