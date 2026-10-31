import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
base='productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020'
for extra in ['','+mgmt_rating_2023','+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+C(region)+listed']:
    m=smf.ols(base+extra,d).fit(cov_type='HC1');print(extra[:30],m.params['training_hours'],m.bse['training_hours'])
print(d[['training_hours','mgmt_rating_2023','productivity_2023','productivity_2020']].corr())
