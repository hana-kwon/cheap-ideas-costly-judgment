import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
specs={
'naive':'productivity_2023~training_hours',
'pre_controls':'productivity_2023~training_hours+'+pre,
'basic':'productivity_2023~training_hours+log_employees_2020+firm_age_2020+C(sector)+C(region)',
'lagged_only':'productivity_2023~training_hours+productivity_2020',
'with_mgmt(post-treatment)':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'log_y':'np.log(productivity_2023)~training_hours+'+pre,
'quad':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
'interact_sector':'productivity_2023~training_hours*C(sector)+'+pre,
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'],m.nobs)
m=smf.ols(specs['pre_controls'],d).fit(cov_type='HC1');print(m.summary())
print(d[['training_hours','mgmt_rating_2023','productivity_2020','productivity_2023']].corr())
