import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020"
allp=pre+"+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
for n,f in [("naive","productivity_2023~training_hours"),("pre",f"productivity_2023~training_hours+{pre}"),("allpre",f"productivity_2023~training_hours+{allp}"),("withmgmt",f"productivity_2023~training_hours+{pre}+mgmt_rating_2023")]:
    r=smf.ols(f,d).fit(cov_type='HC1');print(n,r.params['training_hours'],r.bse['training_hours'])
print(d[['training_hours','productivity_2023','mgmt_rating_2023']].corr())
