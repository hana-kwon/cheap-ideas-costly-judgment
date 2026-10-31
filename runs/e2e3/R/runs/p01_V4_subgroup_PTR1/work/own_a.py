import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
specs={
'naive':'productivity_2023~training_hours',
'size_age_p0':'productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020',
'full_pre':'productivity_2023~training_hours+'+pre,
'full_pre+mgmt':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'logY_full_pre':'np.log(productivity_2023)~training_hours+'+pre,
'full_pre_nolagY':'productivity_2023~training_hours+'+pre.replace('productivity_2020+',''),
'full_pre_quad':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'],len(m.resid))
m=smf.ols(specs['full_pre'],d).fit(cov_type='HC1');print(m.summary())
# tests of nonlinearity / interactions
m2=smf.ols('productivity_2023~training_hours*C(sector)+'+pre,d).fit(cov_type='HC1');print(m2.params.filter(like='training'),m2.pvalues.filter(like='training'))
print(d.corr(numeric_only=True)['training_hours'])
