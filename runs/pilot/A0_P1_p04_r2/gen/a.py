import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+listed+C(region)+C(sector)"
specs={
'naive':'productivity_2023~training_hours',
'lagprod':'productivity_2023~training_hours+productivity_2020',
'pre_full':'productivity_2023~training_hours+'+pre,
'full_plus_mgmt':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'naive_plus_mgmt':'productivity_2023~training_hours+mgmt_rating_2023',
'log_pre_full':'np.log(productivity_2023)~training_hours+'+pre,
'quad_pre_full':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'],m.nobs)
print(d[['training_hours','mgmt_rating_2023','productivity_2020','productivity_2023']].corr())
