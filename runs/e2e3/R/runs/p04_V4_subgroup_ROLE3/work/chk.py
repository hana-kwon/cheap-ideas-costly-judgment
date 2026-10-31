import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.region.value_counts()); print(df.isna().sum().sum())
print(df.training_hours.describe())
f="productivity_2023 ~ training_hours"
c=" + log_employees_2020 + firm_age_2020 + productivity_2020"
c2=c+" + export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+listed"
for name,d in [("all",df)]+[(r,df[df.region==r]) for r in ["north","central","south"]]:
    for lab,form in [("raw",f),("c",f+c),("c2",f+c2)]:
        m=smf.ols(form,d).fit(cov_type="HC1")
        print(name,lab,len(d),round(m.params['training_hours'],3),round(m.bse['training_hours'],3),round(m.pvalues['training_hours'],4))
print(df[['training_hours','productivity_2023','productivity_2020','mgmt_rating_2023','export_share_2020','rd_intensity_2020','credit_score_2020']].corr().round(2))
