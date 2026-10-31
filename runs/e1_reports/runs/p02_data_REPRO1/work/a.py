import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
specs={
'naive':f'{y}~remote_share',
'lagged_outcome':f'{y}~remote_share+patents_per_100_eng_2020',
'size_age_lag':f'{y}~remote_share+patents_per_100_eng_2020+log_engineers_2020+firm_age_2020',
'full_pre':f'{y}~remote_share+{pre}',
'full_pre+collab':f'{y}~remote_share+{pre}+collab_index_2023',
'no_lag_full':f'{y}~remote_share+'+pre.replace('patents_per_100_eng_2020+',''),
}
n=0
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1');n+=1
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],m.nobs)
m=smf.ols(f'collab_index_2023~remote_share+{pre}',d).fit(cov_type='HC1');print('collab on remote',m.params['remote_share'],m.pvalues['remote_share'])
m=smf.ols(f'remote_share~{pre}',d).fit();print(m.summary().tables[1])
# nonlinearity / trimmed
d['rs2']=d.remote_share**2
m=smf.ols(f'{y}~remote_share+rs2+{pre}',d).fit(cov_type='HC1');print(m.params[['remote_share','rs2']],m.pvalues[['remote_share','rs2']])
m=smf.ols(f'{y}~remote_share*C(segment)+{pre}',d).fit(cov_type='HC1');print(m.params.filter(like='remote'),m.pvalues.filter(like='remote'))
