import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020"
pre2=pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for n,f in [("none","productivity_2023~training_hours"),("pre","productivity_2023~training_hours+"+pre),("pre2","productivity_2023~training_hours+"+pre2),("mgmt","productivity_2023~training_hours+"+pre+"+mgmt_rating_2023")]:
    r=smf.ols(f,d).fit(cov_type='HC1');print(n,r.params['training_hours'],r.bse['training_hours'])
print(smf.ols("mgmt_rating_2023~training_hours+productivity_2023+"+pre,d).fit().params)
print(d.corr(numeric_only=True)['mgmt_rating_2023'])
