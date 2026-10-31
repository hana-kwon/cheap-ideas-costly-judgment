import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+listed"
specs={
'1 naive':'productivity_2023~training_hours',
'2 +productivity_2020':'productivity_2023~training_hours+productivity_2020',
'3 all pre controls':f'productivity_2023~training_hours+{pre}',
'4 pre + region + sector':f'productivity_2023~training_hours+{pre}+C(region)+C(sector)',
'5 +mgmt (post-treatment, not preferred)':f'productivity_2023~training_hours+{pre}+C(region)+C(sector)+mgmt_rating_2023',
'6 log outcome, full pre':f'np.log(productivity_2023)~training_hours+{pre}+C(region)+C(sector)',
'7 quadratic':f'productivity_2023~training_hours+I(training_hours**2)+{pre}+C(region)+C(sector)',
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'])
