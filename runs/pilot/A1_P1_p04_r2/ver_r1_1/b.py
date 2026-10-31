import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
m=smf.ols('productivity_2023~training_hours+'+pre,d).fit(cov_type='HC1');print(m.summary())
print(d.describe().T)
for s,g in d.groupby('sector'):
    print(s,smf.ols('productivity_2023~training_hours+'+pre.replace('+C(sector)',''),g).fit(cov_type='HC1').params['training_hours'])
m2=smf.ols('productivity_2023~training_hours*productivity_2020+'+pre,d).fit(cov_type='HC1');print(m2.params['training_hours:productivity_2020'],m2.pvalues['training_hours:productivity_2020'])
print(d.corr(numeric_only=True)['training_hours'])
