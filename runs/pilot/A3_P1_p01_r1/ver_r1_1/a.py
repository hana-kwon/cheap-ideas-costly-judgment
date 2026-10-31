import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
S={'raw':'productivity_2023~training_hours',
'basic':'productivity_2023~training_hours+productivity_2020',
'pre_all':'productivity_2023~training_hours+'+pre,
'pre_all+mgmt':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'log_y_pre':'np.log(productivity_2023)~training_hours+'+pre,
'quad_pre':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
'interact_sector':'productivity_2023~training_hours*C(sector)+'+pre}
for k,f in S.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'],m.rsquared)
print(smf.ols(S['pre_all'],d).fit(cov_type='HC1').summary())
print(d[['training_hours','mgmt_rating_2023','productivity_2020','productivity_2023']].corr())
