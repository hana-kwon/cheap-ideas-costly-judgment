import pandas as pd, numpy as np, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="training_hours+log_employees_2020+firm_age_2020+productivity_2020"
pre2=pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+listed"
def f(fm,d,l):
    r=smf.ols(fm,d).fit(cov_type="HC1");print(l,len(d),round(r.params['training_hours'],3),round(r.bse['training_hours'],3),round(r.pvalues['training_hours'],4))
f("productivity_2023~training_hours",df,"raw all")
f("productivity_2023~"+pre,df,"pre all")
f("productivity_2023~"+pre2,df,"pre2 all")
f("productivity_2023~"+pre2+"+C(region)",df,"pre2 all+region")
for r in ['north','central','south']:
    f("productivity_2023~"+pre2,df[df.region==r],r)
    f("productivity_2023~"+pre,df[df.region==r],r+" pre")
f("productivity_2023~"+pre2+"+mgmt_rating_2023+C(region)",df,"with mgmt")
print(df.isna().sum().sum()); print(df.describe().T)
print(df.groupby('region').training_hours.mean())
