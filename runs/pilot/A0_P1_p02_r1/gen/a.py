import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
specs={
'raw':'remote_share',
'basic':'remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020',
'full_pre':'remote_share+'+pre,
'full_pre+collab(mediator)':'remote_share+collab_index_2023+'+pre,
'full_pre+interactions_region':'remote_share*C(region)+'+pre,
'quad':'remote_share+I(remote_share**2)+'+pre,
}
for k,f in specs.items():
    m=smf.ols(y+'~'+f,d).fit(cov_type='HC1')
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],len(m.resid))
m=smf.ols(y+'~remote_share+'+pre,d[d.remote_share.between(d.remote_share.quantile(.01),d.remote_share.quantile(.99))]).fit(cov_type='HC1')
print('trim',m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
m=smf.ols('collab_index_2023~remote_share+'+pre,d).fit(cov_type='HC1');print('collab',m.params['remote_share'],m.pvalues['remote_share'])
m=smf.ols('remote_share~'+pre,d).fit();print(m.summary().tables[1])
