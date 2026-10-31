import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
print(d.corr(numeric_only=True)['training_hours'])
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
specs={
'raw':'productivity_2023~training_hours',
'basic':'productivity_2023~training_hours+productivity_2020',
'pre':'productivity_2023~training_hours+'+pre,
'pre+mgmt':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'logY pre':'np.log(productivity_2023)~training_hours+'+pre,
'pre+quad':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
'pre+inter sector':'productivity_2023~training_hours*C(sector)+'+pre,
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'],m.nobs)
m=smf.ols(specs['pre'],d).fit(cov_type='HC1');print(m.summary())
print(d.productivity_2023.describe())
