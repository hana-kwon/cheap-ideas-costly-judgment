import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
specs={'raw':'remote_share',
'size_age':'remote_share+log_engineers_2020+firm_age_2020',
'lagged_y':'remote_share+patents_per_100_eng_2020',
'full_pre':'remote_share+'+pre,
'full_pre+collab(mediator)':'remote_share+collab_index_2023+'+pre,
'quad':'remote_share+I(remote_share**2)+'+pre}
for k,f in specs.items():
    m=smf.ols(y+'~'+f,d).fit(cov_type='HC1')
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],m.nobs)
m=smf.ols(y+'~remote_share*C(segment)+'+pre.replace('+C(segment)',''),d).fit(cov_type='HC1');print(m.summary().tables[1])
m=smf.ols('collab_index_2023~remote_share+'+pre,d).fit(cov_type='HC1');print(m.params['remote_share'],m.pvalues['remote_share'])
print(smf.ols(y+'~remote_share+'+pre,d).fit(cov_type='HC1').summary().tables[1])
