import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum())
base='productivity_2023 ~ training_hours + log_employees_2020 + firm_age_2020'
pre=base+' + productivity_2020 + export_share_2020 + foreign_owned + family_owned + rd_intensity_2020 + union_share_2020 + credit_score_2020 + C(sector)+C(region)+listed'
for n,f in [('base',base),('pre_prod',base+'+productivity_2020'),('full_pre',pre),('with_mgmt',pre+'+mgmt_rating_2023')]:
    for d,l in [(df,'full')]:
        r=smf.ols(f,d).fit(cov_type='HC1'); print(n,l,r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
print(df[['training_hours','productivity_2020','mgmt_rating_2023','productivity_2023']].corr())
