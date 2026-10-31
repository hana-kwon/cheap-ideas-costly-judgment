import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
print(d.corr(numeric_only=True).round(2)['training_hours'])
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
specs={
'raw':'productivity_2023~training_hours',
'lagged':'productivity_2023~training_hours+productivity_2020',
'pre_all':'productivity_2023~training_hours+'+pre,
'pre_all_mgmt':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'log_pre':'np.log(productivity_2023)~training_hours+'+pre,
'pre_quad':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
'mgmt_only':'productivity_2023~training_hours+mgmt_rating_2023',
'inter_sector':'productivity_2023~training_hours*C(sector)+'+pre,
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'].round(4),m.bse['training_hours'].round(4),m.pvalues['training_hours'].round(5),round(m.rsquared,3))
print(smf.ols(specs['pre_all'],d).fit(cov_type='HC1').summary())
print(smf.ols('mgmt_rating_2023~training_hours+'+pre,d).fit(cov_type='HC1').params['training_hours'])
