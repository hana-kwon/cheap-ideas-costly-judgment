import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
specs={
'1 naive':'productivity_2023~training_hours',
'2 +size,age,prod2020':'productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020',
'3 all pre-period controls':'productivity_2023~training_hours+'+pre,
'4 pre + mgmt_rating (post)':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'5 pre, quadratic':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
'6 pre, log prod':'np.log(productivity_2023)~training_hours+'+pre,
'7 pre, no lagged prod':'productivity_2023~training_hours+'+pre.replace('productivity_2020+',''),
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'],m.nobs)
    if k.startswith('5'): print(m.params['I(training_hours ** 2)'],m.pvalues['I(training_hours ** 2)'])
m=smf.ols('training_hours~'+pre,d).fit(); print(m.rsquared)
print(smf.ols('mgmt_rating_2023~training_hours+'+pre,d).fit().params['training_hours'])
