import pandas as pd, statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
f="productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020"
for r in [None,'north','central','south']:
    d=df if r is None else df[df.region==r]
    m=smf.ols(f,d).fit(cov_type="HC1")
    print(r,len(d),m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'])
f2=f+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+listed+C(region)"
m=smf.ols(f2,df).fit(cov_type="HC1")
print('full',m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'])
m=smf.ols("productivity_2023~training_hours*C(region)+log_employees_2020+firm_age_2020+productivity_2020",df).fit(cov_type="HC1")
print(m.summary().tables[1])
print(df.training_hours.describe(), df.productivity_2023.describe())
