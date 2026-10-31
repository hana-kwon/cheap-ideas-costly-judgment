import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
allc=pre+'+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
specs={'raw':'',
'pre3':'+'+pre,
'all_pre':'+'+allc,
'all_pre_plus_collab(post-treatment)':'+'+allc+'+collab_index_2023',
'no_lagged_outcome':'+log_engineers_2020+firm_age_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'}
for k,v in specs.items():
    m=smf.ols(f'{y}~remote_share{v}',d).fit(cov_type='HC3')
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],m.nobs)
m=smf.ols(f'{y}~remote_share+'+allc,d).fit(cov_type='HC3');print(m.summary())
m=smf.ols(f'collab_index_2023~remote_share+'+allc,d).fit(cov_type='HC3');print('collab on remote',m.params['remote_share'],m.pvalues['remote_share'])
