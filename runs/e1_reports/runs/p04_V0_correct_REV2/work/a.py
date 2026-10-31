import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="log_employees_2020+firm_age_2020+productivity_2020"
allp=pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for n,f in [("none","productivity_2023~training_hours"),("analyst","productivity_2023~training_hours+"+pre),("allpre","productivity_2023~training_hours+"+allp),("withmgmt","productivity_2023~training_hours+mgmt_rating_2023+"+allp)]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(n,r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
print(df.isna().sum().sum()); print(df.corr(numeric_only=True)['training_hours'])
