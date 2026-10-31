import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="training_hours+log_employees_2020+firm_age_2020+productivity_2020"
allc=pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+listed+C(region)"
def f(d,form,l):
    m=smf.ols(form,d).fit(cov_type="HC1");print(l,len(d),round(m.params['training_hours'],3),round(m.bse['training_hours'],3),round(m.pvalues['training_hours'],4))
f(df,"productivity_2023~training_hours","raw all")
f(df,"productivity_2023~"+pre,"pre all")
f(df,"productivity_2023~"+allc,"allc all")
for r in df.region.unique():
    d=df[df.region==r]; f(d,"productivity_2023~"+pre,r); f(d,"productivity_2023~"+allc.replace("+C(region)",""),r+" allc")
f(df,"productivity_2023~"+allc+"+mgmt_rating_2023","with mgmt")
print(df.isna().sum().sum()); print(df.groupby('region').training_hours.mean())
