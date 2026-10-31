import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="productivity_2023~training_hours+productivity_2020+log_employees_2020+firm_age_2020+C(sector)+listed+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
for r in ['north','central','south']:
    m=smf.ols(f,df[df.region==r]).fit(cov_type="HC1")
    print(r,(df.region==r).sum(),m.params['training_hours'],m.bse['training_hours'])
m=smf.ols(f+"+C(region)",df).fit(cov_type="HC1");print('all',m.params['training_hours'],m.bse['training_hours'])
m=smf.ols("productivity_2023~training_hours+productivity_2020+log_employees_2020+firm_age_2020",df[df.region=='north']).fit(cov_type="HC1");print('north untrimmed',m.params['training_hours'],m.bse['training_hours'])
