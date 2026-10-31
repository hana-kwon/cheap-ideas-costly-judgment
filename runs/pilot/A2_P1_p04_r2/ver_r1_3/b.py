import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed"
for s in ['manufacturing','services']:
    m=smf.ols('productivity_2023~training_hours+'+pre,d[d.sector==s]).fit(cov_type='HC1');print(s,m.params['training_hours'],m.bse['training_hours'],len(d[d.sector==s]))
m=smf.ols('productivity_2023~training_hours*C(sector)+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
m=smf.ols('productivity_2023~training_hours+'+pre+'+C(sector)',d).fit(cov_type='HC1');print(m.params['training_hours'],m.bse['training_hours'])
