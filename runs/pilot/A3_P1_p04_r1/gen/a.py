import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
S={'raw':'productivity_2023~training_hours',
'core':'productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020',
'full_pre':'productivity_2023~training_hours+'+pre,
'full_pre+mgmt':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'logY_full_pre':'np.log(productivity_2023)~training_hours+'+pre,
'quad_full_pre':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
'no_lagY':'productivity_2023~training_hours+'+pre.replace('+productivity_2020',''),
}
for k,f in S.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'],m.nobs)
    if k=='quad_full_pre': print(m.params['I(training_hours ** 2)'],m.pvalues['I(training_hours ** 2)'])
m=smf.ols('productivity_2023~training_hours+'+pre,d).fit(cov_type='HC1');print(m.summary())
print(d.productivity_2023.describe())
