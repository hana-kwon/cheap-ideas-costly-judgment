import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
specs={
'naive':f'{y}~remote_share',
'size_age':f'{y}~remote_share+log_engineers_2020+firm_age_2020',
'lagged_y':f'{y}~remote_share+patents_per_100_eng_2020',
'full_pre':f'{y}~remote_share+{pre}',
'full_pre+collab(mediator)':f'{y}~remote_share+{pre}+collab_index_2023',
'collab_only':f'{y}~remote_share+collab_index_2023',
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,round(m.params['remote_share'],4),round(m.bse['remote_share'],4),m.pvalues['remote_share'],int(m.nobs))
m=smf.ols(f'{y}~remote_share+{pre}',d).fit(cov_type='HC1');print(m.summary())
print(smf.ols('remote_share~'+pre,d).fit().summary().tables[1])
print(smf.ols(f'collab_index_2023~remote_share+{pre}',d).fit().params['remote_share'])
# robustness: interactions, trimmed
d2=d[(d.remote_share>d.remote_share.quantile(.01))&(d.remote_share<d.remote_share.quantile(.99))]
m=smf.ols(f'{y}~remote_share+{pre}',d2).fit(cov_type='HC1');print('trim',m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
m=smf.ols(f'{y}~remote_share+I(remote_share**2)+{pre}',d).fit(cov_type='HC1');print('quad',m.params[['remote_share','I(remote_share ** 2)']],m.pvalues[['remote_share','I(remote_share ** 2)']])
