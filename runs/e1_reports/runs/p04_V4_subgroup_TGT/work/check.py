import pandas as pd
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
c='training_hours + log_employees_2020 + firm_age_2020 + productivity_2020'
c2=c+' + export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+listed+C(region)'
for name,d in [('full',df),('north',df[df.region=='north'])]:
    for f in [c,c2]:
        r=smf.ols('productivity_2023 ~ '+f,d).fit(cov_type='HC1')
        print(name,len(d),r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
print(df.groupby('region').size())
for g,d in df.groupby('region'):
    r=smf.ols('productivity_2023 ~ '+c,d).fit(cov_type='HC1')
    print(g,r.params['training_hours'],r.pvalues['training_hours'])
