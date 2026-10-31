import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
pre='log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+listed+C(region)+C(sector)'
specs={
'naive':'productivity_2023~training_hours',
'lag_prod':'productivity_2023~training_hours+productivity_2020',
'pre_controls':'productivity_2023~training_hours+'+pre,
'pre+mgmt(bad control)':'productivity_2023~training_hours+mgmt_rating_2023+'+pre,
'pre_no_lag':'productivity_2023~training_hours+'+pre.replace('productivity_2020+',''),
}
for k,f in specs.items():
    r=smf.ols(f,d).fit(cov_type='HC1')
    print(k,r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'],r.nobs)
d['lp']=pd.np.log(d.productivity_2023) if hasattr(pd,'np') else 0
import numpy as np
d['lp']=np.log(d.productivity_2023)
r=smf.ols('lp~training_hours+'+pre,d).fit(cov_type='HC1')
print('log',r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
r=smf.ols('productivity_2023~training_hours*C(sector)+'+pre,d).fit(cov_type='HC1')
print(r.summary().tables[1])
print(d[['training_hours','mgmt_rating_2023','productivity_2023','productivity_2020']].corr())
