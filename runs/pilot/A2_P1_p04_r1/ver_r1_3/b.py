import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
m=smf.ols('productivity_2023~training_hours+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
print(d.describe().T)
print(d[['training_hours','mgmt_rating_2023','productivity_2020','productivity_2023']].corr())
print(smf.ols('mgmt_rating_2023~training_hours+productivity_2023',d).fit().params)
print(smf.ols('training_hours~'+pre,d).fit().rsquared)
for s in ['manufacturing','services']:
    print(s,smf.ols('productivity_2023~training_hours+'+pre,d[d.sector==s]).fit(cov_type='HC1').params['training_hours'])
