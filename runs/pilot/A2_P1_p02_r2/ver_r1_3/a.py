import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
allpre=pre+'+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
specs={'raw':'remote_share','basic':'remote_share+'+pre,'pre+cat':'remote_share+'+pre+'+C(region)+listed+C(segment)',
'full':'remote_share+'+allpre,'full+collab(mediator)':'remote_share+'+allpre+'+collab_index_2023',
'no lagged outcome':'remote_share+log_engineers_2020+firm_age_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'}
for k,f in specs.items():
    m=smf.ols(y+'~'+f,d).fit(cov_type='HC1')
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],m.nobs)
m=smf.ols(y+'~remote_share+'+allpre+'+remote_share:C(segment)',d).fit(cov_type='HC1');print(m.summary().tables[1])
m=smf.ols(y+'~remote_share+I(remote_share**2)+'+allpre,d).fit(cov_type='HC1');print(m.params[['remote_share','I(remote_share ** 2)']],m.pvalues[['remote_share','I(remote_share ** 2)']])
print(smf.ols('remote_share~'+allpre,d).fit().summary().tables[1])
print(d[['remote_share','collab_index_2023',y]].corr())
