import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
flex=pre+"+I(log_employees_2020**2)+I(firm_age_2020**2)+I(productivity_2020**2)+log_employees_2020:productivity_2020+firm_age_2020:productivity_2020+log_employees_2020:firm_age_2020"
m=smf.ols('productivity_2023~training_hours+'+flex,d).fit(cov_type='HC1');print(m.params['training_hours'],m.bse['training_hours'])
m=smf.ols('productivity_2023~training_hours+'+pre,d).fit()
print(m.summary().tables[1])
