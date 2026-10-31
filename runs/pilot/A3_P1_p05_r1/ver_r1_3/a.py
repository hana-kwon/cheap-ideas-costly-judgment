import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
specs={'naive':'1','lagged_only':'patents_per_100_eng_2020','size_age':'log_engineers_2020+firm_age_2020','full_pre':pre,
'full_pre+collab':pre+'+collab_index_2023','collab_only':'collab_index_2023'}
y='patents_per_100_eng_2023'
for k,v in specs.items():
    m=smf.ols(f'{y}~remote_share+{v}',d).fit(cov_type='HC3')
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],m.nobs)
d['ly']=np.log(d[y])
m=smf.ols(f'ly~remote_share+{pre}',d).fit(cov_type='HC3');print('log',m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
m=smf.ols(f'{y}~remote_share*C(segment)+{pre}',d).fit(cov_type='HC3');print(m.summary().tables[1])
m=smf.ols(f'{y}~remote_share+I(remote_share**2)+{pre}',d).fit(cov_type='HC3');print(m.params['remote_share'],m.pvalues[['remote_share','I(remote_share ** 2)']])
print(smf.ols(f'remote_share~collab_index_2023+{pre}',d).fit().params['collab_index_2023'])
print(smf.ols(f'{y}~remote_share+{pre}',d).fit(cov_type='HC3').summary().tables[1])
