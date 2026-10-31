import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
m=smf.ols('productivity_2023~training_hours+'+pre,d).fit(cov_type='HC1');print(m.summary())
print(d.corr(numeric_only=True).round(2).to_string())
m=smf.ols('mgmt_rating_2023~training_hours+productivity_2023+'+pre,d).fit();print(m.params[['training_hours','productivity_2023']])
m=smf.ols('productivity_2023~training_hours*C(sector)+'+pre,d).fit(cov_type='HC1');print(m.params.filter(like='training'),m.pvalues.filter(like='training'))
