import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
base='productivity_2023 ~ training_hours'
pre='+productivity_2020+log_employees_2020+firm_age_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)'
for f in [base,base+pre,base+pre+'+mgmt_rating_2023']:
    print(smf.ols(f,d).fit(cov_type='HC1').summary().tables[1])
print(d.corr(numeric_only=True)['training_hours'])
