import pandas as pd, statsmodels.formula.api as smf, numpy as np
d=pd.read_csv('data.csv')
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
for f in ['productivity_2023~training_hours+'+pre,
 'productivity_2023~training_hours+'+pre+'+I(log_employees_2020**2)+I(firm_age_2020**2)+I(productivity_2020**2)+productivity_2020:log_employees_2020']:
    m=smf.ols(f,d).fit(cov_type='HC1');print(m.params['training_hours'],m.pvalues['training_hours'])
q=d[(d.training_hours.abs()<3)&(d.productivity_2023.between(d.productivity_2023.quantile(.01),d.productivity_2023.quantile(.99)))]
m=smf.ols('productivity_2023~training_hours+'+pre,q).fit(cov_type='HC1');print(m.params['training_hours'],m.pvalues['training_hours'])
