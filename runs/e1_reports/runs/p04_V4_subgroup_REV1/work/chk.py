import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+listed+C(region)'
for name,f,df in [('raw','productivity_2023~training_hours',d),('basic','productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020',d),('full','productivity_2023~training_hours+'+pre,d)]+[('reg_'+r,'productivity_2023~training_hours+'+pre.replace('+C(region)',''),d[d.region==r]) for r in ['north','central','south']]:
    m=smf.ols(f,df).fit(cov_type='HC1');print(name,len(df),m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'])
print(d.isna().sum().sum())
