import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.corr(numeric_only=True)['training_hours'])
base="productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020"
pre=base+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for f in [ "productivity_2023~training_hours",base,base+"+mgmt_rating_2023",pre,pre+"+mgmt_rating_2023"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(r.params['training_hours'],r.bse['training_hours'])
print(smf.ols("mgmt_rating_2023~training_hours+productivity_2020",df).fit().summary().tables[1])
