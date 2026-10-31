import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed"
for s,g in d.groupby('sector'):
    m=smf.ols('productivity_2023~training_hours+'+pre,g).fit(cov_type='HC1');print(s,len(g),m.params['training_hours'],m.bse['training_hours'])
m=smf.ols('training_hours~'+pre+'+C(sector)',d).fit();print(m.summary().tables[1])
