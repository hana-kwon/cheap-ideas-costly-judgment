import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_employees_2020+firm_age_2020+productivity_2020'
allc=pre+'+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)'
for f in ['training_hours',f'training_hours+{pre}',f'training_hours+{allc}',f'training_hours+{pre}+mgmt_rating_2023',f'training_hours+{allc}+mgmt_rating_2023']:
    r=smf.ols('productivity_2023~'+f,d).fit(cov_type='HC1');print(r.params['training_hours'],r.bse['training_hours'])
print(d[['training_hours','mgmt_rating_2023','productivity_2023']].corr())
