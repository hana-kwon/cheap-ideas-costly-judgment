import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
b='productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020'
pre='+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)'
for n,f in [('naive','productivity_2023~training_hours'),('base',b),('base+m',b+'+mgmt_rating_2023'),('pre',b+pre),('pre+m',b+pre+'+mgmt_rating_2023')]:
    r=smf.ols(f,d).fit(cov_type='HC1');print(n,r.params['training_hours'],r.bse['training_hours'])
print(d[['training_hours','mgmt_rating_2023','productivity_2023']].corr())
