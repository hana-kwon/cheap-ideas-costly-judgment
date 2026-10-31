import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
f='patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
for ff in [f, f+'+collab_index_2023']:
    m=smf.ols(ff,d).fit(cov_type='HC1');print(m.params.filter(regex='remote|collab'),m.pvalues.filter(regex='remote|collab'))
print(d[['remote_share','collab_index_2023','patents_per_100_eng_2023']].corr())
print(d.isna().sum().sum(), d.remote_share.describe())
for s,g in d.groupby('segment'):
    print(s,smf.ols(f.replace('+C(segment)',''),g).fit(cov_type='HC1').params['remote_share'])
d['rq']=pd.qcut(d.remote_share,5,labels=False)
print(smf.ols(f.replace('remote_share','C(rq)'),d).fit(cov_type='HC1').params.filter(like='rq'))
