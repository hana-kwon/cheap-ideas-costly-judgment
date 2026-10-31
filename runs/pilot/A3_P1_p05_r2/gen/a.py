import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
pre="log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
specs={'raw':'',
'size/age':'+log_engineers_2020+firm_age_2020',
'lagged outcome':'+patents_per_100_eng_2020',
'full pre':'+'+pre,
'full pre + collab (post)':'+'+pre+'+collab_index_2023',
'collab only':'+collab_index_2023'}
for k,v in specs.items():
    m=smf.ols('patents_per_100_eng_2023~remote_share'+v,d).fit(cov_type='HC1')
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],len(d))
m=smf.ols('collab_index_2023~remote_share+'+pre,d).fit(cov_type='HC1');print('collab on remote',m.params['remote_share'],m.pvalues['remote_share'])
m=smf.ols('remote_share~'+pre,d).fit();print(m.summary().tables[1])
d['r2']=d.remote_share**2
m=smf.ols('patents_per_100_eng_2023~remote_share+r2+'+pre,d).fit(cov_type='HC1');print(m.params[['remote_share','r2']],m.pvalues[['remote_share','r2']])
m=smf.ols('patents_per_100_eng_2023~remote_share*C(segment)+'+pre,d).fit(cov_type='HC1');print(m.params.filter(like='remote'),m.pvalues.filter(like='remote'))
d['lp']=np.log(d.patents_per_100_eng_2023)
m=smf.ols('lp~remote_share+'+pre,d).fit(cov_type='HC1');print('log',m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
