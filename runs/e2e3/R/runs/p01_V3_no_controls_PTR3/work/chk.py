import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
for f in ['productivity_2023~training_hours','productivity_2023~training_hours+'+pre]:
    m=smf.ols(f,d).fit(cov_type='HC1');print(m.params['training_hours'],m.bse['training_hours'])
