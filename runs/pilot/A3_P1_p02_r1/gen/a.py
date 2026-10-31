import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
specs={'raw':'remote_share',
'basic':'remote_share+log_engineers_2020+firm_age_2020',
'lagged outcome':'remote_share+patents_per_100_eng_2020',
'basic+lag+region+seg+listed':'remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+C(segment)+listed',
'full pre':'remote_share+'+pre,
'full pre+collab (post-treatment)':'remote_share+collab_index_2023+'+pre,
'no lag, full other':'remote_share+'+pre.replace('+patents_per_100_eng_2020',''),
}
for k,f in specs.items():
    m=smf.ols(y+'~'+f,d).fit(cov_type='HC1')
    print(k,round(m.params['remote_share'],4),round(m.bse['remote_share'],4),m.pvalues['remote_share'],int(m.nobs))
m=smf.ols('collab_index_2023~remote_share+'+pre,d).fit(cov_type='HC1');print('collab on remote',m.params['remote_share'],m.pvalues['remote_share'])
m=smf.ols('remote_share~'+pre,d).fit();print(m.summary().tables[1])
