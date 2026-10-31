import numpy as np, pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
pre='log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020'
specs={'raw':'productivity_2023~training_hours',
'basic':'productivity_2023~training_hours+log_employees_2020+firm_age_2020+C(region)+C(sector)+listed',
'pre_full':'productivity_2023~training_hours+'+pre,
'pre_full+mgmt':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'lagged_only':'productivity_2023~training_hours+productivity_2020',
'logY_pre_full':'np.log(productivity_2023)~training_hours+'+pre,
'pre_full+sq':'productivity_2023~training_hours+I(training_hours**2)+'+pre}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'],m.nobs)
print(smf.ols('training_hours~'+pre+'+mgmt_rating_2023',d).fit().summary().tables[1])
