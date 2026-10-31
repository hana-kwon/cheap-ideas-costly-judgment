import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
specs={
'naive':f'{y}~remote_share',
'size_age':f'{y}~remote_share+log_engineers_2020+firm_age_2020',
'lagged_y':f'{y}~remote_share+patents_per_100_eng_2020',
'full_pre':f'{y}~remote_share+{pre}',
'full_pre+collab(post-treatment)':f'{y}~remote_share+{pre}+collab_index_2023',
'collab_only':f'{y}~remote_share+collab_index_2023',
'full_pre_quad':f'{y}~remote_share+I(remote_share**2)+{pre}',
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],m.nobs)
m=smf.ols(f'remote_share~{pre}+collab_index_2023',d).fit();print(m.summary().tables[1])
m=smf.ols(f'collab_index_2023~remote_share+{pre}',d).fit();print(m.params['remote_share'],m.pvalues['remote_share'])
# robust: interactions
m=smf.ols(f'{y}~remote_share*C(segment)+{pre}',d).fit(cov_type='HC1');print(m.params.filter(like='remote'),m.pvalues.filter(like='remote'))
