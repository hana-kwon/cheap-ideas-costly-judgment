import numpy as np, pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020'
m=smf.ols('productivity_2023~training_hours+I(training_hours**2)+'+pre,d).fit(cov_type='HC1')
print(m.summary().tables[1])
print(d.training_hours.describe())
m=smf.ols('productivity_2023~training_hours*C(sector)+training_hours*C(region)+'+pre,d).fit(cov_type='HC1')
print(m.summary().tables[1])
print(d[['training_hours','mgmt_rating_2023','productivity_2023','productivity_2020','log_employees_2020']].corr())
d['q']=pd.qcut(d.training_hours,5,labels=False)
print(smf.ols('productivity_2023~C(q)+'+pre,d).fit(cov_type='HC1').params[:5])
