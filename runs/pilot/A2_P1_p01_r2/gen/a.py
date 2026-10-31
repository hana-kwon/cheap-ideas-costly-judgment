import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
specs={
'naive':'productivity_2023~training_hours',
'lagged_prod':'productivity_2023~training_hours+productivity_2020',
'size_age_sector_region':'productivity_2023~training_hours+productivity_2020+log_employees_2020+firm_age_2020+C(region)+C(sector)+listed',
'full_pre':'productivity_2023~training_hours+'+pre,
'full_pre_plus_mgmt':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'full_pre_quad':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
'log_outcome_full':'np.log(productivity_2023)~training_hours+'+pre,
'full_no_lag':'productivity_2023~training_hours+'+pre.replace('+productivity_2020',''),
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,round(m.params['training_hours'],4),round(m.bse['training_hours'],4),m.pvalues['training_hours'])
m=smf.ols(specs['full_pre'],d).fit(cov_type='HC1');print(m.summary().tables[1])
# training determinants
print(smf.ols('training_hours~'+pre,d).fit().summary().tables[1])
print(d[['training_hours','mgmt_rating_2023','productivity_2023']].corr())
