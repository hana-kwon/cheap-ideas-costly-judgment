import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="log_employees_2020+firm_age_2020+productivity_2020"
allc=pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for name,f,d in [("raw","productivity_2023~training_hours",df),("pre","productivity_2023~training_hours+"+pre,df),("allpre","productivity_2023~training_hours+"+allc,df),("allpre+mgmt","productivity_2023~training_hours+mgmt_rating_2023+"+allc,df)]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(name,r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
print(df.corr(numeric_only=True)['training_hours'])
