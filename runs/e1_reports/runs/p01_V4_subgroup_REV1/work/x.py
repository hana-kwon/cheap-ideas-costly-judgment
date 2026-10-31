import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020"
allc=pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+C(region)+listed"
for name,f,s in [("naive","productivity_2023~training_hours",d),("pre","productivity_2023~training_hours+"+pre,d),("all","productivity_2023~training_hours+"+allc,d),
 ("north","productivity_2023~training_hours+"+pre,d[d.region=='north'])]+[(r,"productivity_2023~training_hours+"+allc.replace("+C(region)",""),d[d.region==r]) for r in ['north','central','south']]:
    m=smf.ols(f,s).fit(cov_type='HC1');print(name,len(s),m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'])
