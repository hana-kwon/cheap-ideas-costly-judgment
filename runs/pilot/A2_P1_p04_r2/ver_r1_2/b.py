import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for s,g in d.groupby('sector'):
    m=smf.ols('productivity_2023~training_hours+'+pre.replace('+C(sector)',''),g).fit(cov_type='HC1');print(s,m.params['training_hours'],m.bse['training_hours'],len(g))
m=smf.ols('productivity_2023~training_hours*C(sector)+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
print(smf.ols('training_hours~'+pre,d).fit().summary().tables[1])
