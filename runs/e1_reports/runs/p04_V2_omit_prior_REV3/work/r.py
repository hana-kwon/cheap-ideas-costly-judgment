import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)'
for f in ['productivity_2023~training_hours','productivity_2023~training_hours+log_employees_2020+firm_age_2020','productivity_2023~training_hours+'+pre,'productivity_2023~training_hours+mgmt_rating_2023+'+pre]:
    m=smf.ols(f,d).fit(cov_type='HC1');print(f[:60],m.params['training_hours'],m.bse['training_hours'])
print(smf.ols('training_hours~'+pre,d).fit().summary().tables[1])
