import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y=d.productivity_2023;lo,hi=y.quantile([.01,.99]);t=d[(y>=lo)&(y<=hi)]
f='productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)'
for x in (d,t):
    m=smf.ols(f,x).fit(cov_type='HC1');print(m.params['training_hours'],m.bse['training_hours'],m.params['productivity_2020'])
