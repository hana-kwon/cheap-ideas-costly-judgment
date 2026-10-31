import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum().sum())
base='productivity_2023 ~ training_hours'
pre=' + log_employees_2020 + firm_age_2020 + productivity_2020'
allc=pre+' + export_share_2020 + foreign_owned + family_owned + rd_intensity_2020 + union_share_2020 + credit_score_2020 + C(sector)+C(region)+listed'
for name,f in [('raw',base),('pre',base+pre),('all',base+allc),('all+mgmt',base+allc+'+mgmt_rating_2023')]:
    r=smf.ols(f,df).fit(cov_type='HC1')
    print(name,r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'],len(df))
y=df.productivity_2023;lo,hi=y.quantile([.01,.99]);d=df[(y>=lo)&(y<=hi)]
r=smf.ols(base+allc,d).fit(cov_type='HC1');print('trim all',r.params['training_hours'],r.bse['training_hours'])
print(df[['training_hours','productivity_2023','productivity_2020','export_share_2020','foreign_owned','family_owned','rd_intensity_2020','union_share_2020','credit_score_2020','mgmt_rating_2023']].corr().round(2))
