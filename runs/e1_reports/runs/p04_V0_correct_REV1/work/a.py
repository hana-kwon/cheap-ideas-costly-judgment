import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
b="productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020"
pre="+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for f in [b,b+pre,b+pre+"+mgmt_rating_2023"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
print(df.isna().sum().sum(), df.productivity_2023.describe())
print(df[['training_hours','export_share_2020','foreign_owned','family_owned','rd_intensity_2020','union_share_2020','credit_score_2020','productivity_2020','mgmt_rating_2023']].corr().round(2).iloc[0])
