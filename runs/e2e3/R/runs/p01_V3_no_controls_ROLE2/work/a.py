import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
for name,f in [("none","productivity_2023~training_hours"),("pre","productivity_2023~training_hours+"+pre),("pre+mgmt","productivity_2023~training_hours+mgmt_rating_2023+"+pre),("p2020","productivity_2023~training_hours+productivity_2020")]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(name,r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
print(df[['training_hours','productivity_2020','mgmt_rating_2023','productivity_2023']].corr())
