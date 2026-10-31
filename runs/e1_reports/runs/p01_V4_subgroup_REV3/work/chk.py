import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_employees_2020+firm_age_2020+productivity_2020'
allc=pre+'+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+listed+C(region)'
for name,f,s in [('naive','productivity_2023~training_hours',d),('pre','productivity_2023~training_hours+'+pre,d),('all','productivity_2023~training_hours+'+allc,d),
 ('north','productivity_2023~training_hours+'+pre,d[d.region=='north'])]:
    r=smf.ols(f,s).fit(cov_type='HC1');print(name,len(s),r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
for g,s in d.groupby('region'):
    r=smf.ols('productivity_2023~training_hours+'+allc.replace('+C(region)',''),s).fit(cov_type='HC1');print(g,len(s),r.params['training_hours'],r.pvalues['training_hours'])
