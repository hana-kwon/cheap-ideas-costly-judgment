import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
lo,hi=d.productivity_2023.quantile([.01,.99])
t=d[(d.productivity_2023>=lo)&(d.productivity_2023<=hi)]
for n,x in [('analyst',d),('trim',t)]:
    for f in ['productivity_2023~training_hours+log_employees_2020+firm_age_2020',
              'productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020',
              'productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020']:
        m=smf.ols(f,x).fit(cov_type='HC1');print(n,len(x),m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'])
