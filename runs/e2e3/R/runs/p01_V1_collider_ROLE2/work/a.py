import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_employees_2020+firm_age_2020+productivity_2020'
allp=pre+'+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)'
for n,f in {'raw':'','pre':'+'+pre,'allpre':'+'+allp,'mgmt':'+'+pre+'+mgmt_rating_2023','allmgmt':'+'+allp+'+mgmt_rating_2023'}.items():
    for trim in [0,1]:
        x=d.copy()
        if trim:
            lo,hi=x.productivity_2023.quantile([.01,.99]);x=x[(x.productivity_2023>=lo)&(x.productivity_2023<=hi)]
        r=smf.ols('productivity_2023~training_hours'+f,x).fit(cov_type='HC1')
        print(n,trim,r.params['training_hours'],r.bse['training_hours'])
print(d[['training_hours','mgmt_rating_2023','productivity_2023','productivity_2020']].corr())
