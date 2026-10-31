import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
print(d[y].std())
b='~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
for g in ['region','segment','listed','hq_in_hub_city','vc_backed','founder_ceo']:
    f = y+b+'+remote_share:C(%s)'%g if g in('region','segment') else y+b+'+remote_share:%s+%s'%(g,g)
    r=smf.ols(f,d).fit(cov_type='HC1')
    print(g,r.params.filter(like='remote').round(2).tolist(),r.pvalues.filter(like='remote').round(3).tolist())
r=smf.ols(y+b+'+I(remote_share**2)',d).fit(cov_type='HC1');print(r.pvalues.round(3))
