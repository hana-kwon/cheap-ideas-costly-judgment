import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
S={'raw':'',
'lagged outcome':'+patents_per_100_eng_2020',
'size/age/lag':'+patents_per_100_eng_2020+log_engineers_2020+firm_age_2020',
'full pre-treatment':'+'+pre,
'full + collab (post-treatment, not preferred)':'+'+pre+'+collab_index_2023',
'collab only (not preferred)':'+collab_index_2023',
'full, quadratic':'+'+pre+'+I(remote_share**2)',
}
n=0
for k,v in S.items():
    m=smf.ols(f'{y}~remote_share{v}',d).fit(cov_type='HC3');n+=1
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
m=smf.ols(f'{y}~remote_share+{pre}+remote_share:patents_per_100_eng_2020+remote_share:C(segment)',d).fit(cov_type='HC3');n+=1
print(m.summary().tables[1])
m=smf.ols(f'{y}~remote_share+{pre}',d[d.remote_share.abs()<3]).fit(cov_type='HC3');n+=1
print('trim',m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
print(smf.ols(f'collab_index_2023~remote_share+{pre}',d).fit().params['remote_share'])
print(n)
