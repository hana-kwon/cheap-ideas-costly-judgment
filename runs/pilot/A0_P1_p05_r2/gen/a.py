import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
allc=pre+'+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
specs={'raw':'remote_share','basic':'remote_share+'+pre,'full':'remote_share+'+allc,
'full+collab(mediator)':'remote_share+'+allc+'+collab_index_2023',
'full+interactions_seg':'remote_share*C(segment)+'+allc}
for k,f in specs.items():
    m=smf.ols(y+'~'+f,d).fit(cov_type='HC1')
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],m.nobs)
m=smf.ols(y+'~remote_share+'+allc,d).fit(cov_type='HC1');print(m.summary())
# nonlinear / outcome tail
d['lp']=np.log(d[y].clip(lower=1))
m2=smf.ols('lp~remote_share+'+allc,d).fit(cov_type='HC1');print('log',m2.params['remote_share'],m2.bse['remote_share'],m2.pvalues['remote_share'])
m3=smf.ols(y+'~remote_share+I(remote_share**2)+'+allc,d).fit(cov_type='HC1');print('quad',m3.params[['remote_share','I(remote_share ** 2)']],m3.pvalues[['remote_share','I(remote_share ** 2)']])
print(d[y].describe(), d.isna().sum().sum())
print(smf.ols('remote_share~'+allc,d).fit().summary().tables[1])
