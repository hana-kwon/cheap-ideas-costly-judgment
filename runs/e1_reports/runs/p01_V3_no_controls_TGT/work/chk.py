import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for name,f,d in [("naive","productivity_2023~training_hours",df),
 ("pre","productivity_2023~training_hours+"+pre,df),
 ("pre+mgmt","productivity_2023~training_hours+mgmt_rating_2023+"+pre,df),
 ("lag only","productivity_2023~training_hours+productivity_2020",df)]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(name,r.params['training_hours'],r.bse['training_hours'],len(d))
print(df[['training_hours','mgmt_rating_2023','productivity_2020','productivity_2023']].corr())
