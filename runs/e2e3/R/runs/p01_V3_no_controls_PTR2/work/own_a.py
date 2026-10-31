import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
print(d.corr(numeric_only=True).round(2)[['training_hours','productivity_2023']])
pre='log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)'
specs={
'naive':'productivity_2023~training_hours',
'size_age':'productivity_2023~training_hours+log_employees_2020+firm_age_2020',
'lagprod':'productivity_2023~training_hours+productivity_2020',
'pre_all':'productivity_2023~training_hours+'+pre,
'pre_all+mgmt':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'log_pre_all':'np.log(productivity_2023)~training_hours+'+pre,
'pre_quad':'productivity_2023~training_hours+I(training_hours**2)+'+pre,
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,round(m.params['training_hours'],4),round(m.bse['training_hours'],4),m.pvalues['training_hours'],m.nobs)
m=smf.ols(specs['pre_all'],d).fit(cov_type='HC1');print(m.summary())
