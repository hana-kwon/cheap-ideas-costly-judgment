import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="log_employees_2020+firm_age_2020+productivity_2020"
allc=pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for f in ["productivity_2023~training_hours","productivity_2023~training_hours+"+pre,"productivity_2023~training_hours+"+allc,"productivity_2023~training_hours+"+allc+"+mgmt_rating_2023"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
print(df.drop(columns=['region','sector']).corr()['training_hours'])
