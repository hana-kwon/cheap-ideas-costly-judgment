import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_employees_2020+firm_age_2020+productivity_2020'
full=pre+'+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)'
for n,f in [('none','productivity_2023~training_hours'),('pre','productivity_2023~training_hours+'+pre),('full','productivity_2023~training_hours+'+full),('full+m','productivity_2023~training_hours+'+full+'+mgmt_rating_2023')]:
    r=smf.ols(f,d).fit(cov_type='HC1');print(n,r.params['training_hours'],r.bse['training_hours'])
print(smf.ols('mgmt_rating_2023~training_hours+'+full,d).fit().params['training_hours'])
print(smf.ols('mgmt_rating_2023~productivity_2023+'+full,d).fit().params['productivity_2023'])
