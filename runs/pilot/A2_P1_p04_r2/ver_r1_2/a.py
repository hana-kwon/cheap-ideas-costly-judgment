import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
specs={
'1 naive':'productivity_2023~training_hours',
'2 pre controls':'productivity_2023~training_hours+'+pre,
'3 pre controls+mgmt (post-treatment)':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'4 minimal: size,age,prod2020':'productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020',
'5 log outcome pre controls':'np.log(productivity_2023)~training_hours+'+pre,
'6 pre controls + quadratic':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
'7 pre controls + sector interaction':'productivity_2023~training_hours*C(sector)+'+pre,
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k, m.params['training_hours'], m.bse['training_hours'], m.pvalues['training_hours'], m.nobs)
m=smf.ols(specs['2 pre controls'],d).fit(cov_type='HC1');print(m.summary())
print(d[['training_hours','mgmt_rating_2023','productivity_2023']].corr())
print(smf.ols('mgmt_rating_2023~training_hours+'+pre,d).fit().params['training_hours'])
