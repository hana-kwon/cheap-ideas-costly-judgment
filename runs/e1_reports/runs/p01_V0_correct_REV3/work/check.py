import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
base='productivity_2023 ~ training_hours'
pre=' + log_employees_2020+firm_age_2020+productivity_2020'
pre2=pre+'+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)'
for n,f in [('raw',base),('rep',base+pre),('full',base+pre2),('full+mgmt',base+pre2+'+mgmt_rating_2023')]:
    for t in [0,1]:
        x=d
        if t:
            lo,hi=d.productivity_2023.quantile([.01,.99]);x=d[(d.productivity_2023>=lo)&(d.productivity_2023<=hi)]
        r=smf.ols(f,x).fit(cov_type='HC1');print(n,t,len(x),r.params['training_hours'].round(3),r.bse['training_hours'].round(3),r.pvalues['training_hours'].round(4))
print(d.isna().sum().sum())
print(d[['training_hours','mgmt_rating_2023','productivity_2020','export_share_2020','rd_intensity_2020','credit_score_2020']].corr().round(2))
