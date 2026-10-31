import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv');print(d.describe().T);print(d.isna().sum().sum())
print(d.corr(numeric_only=True)['remote_share'])
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
specs={'raw':'remote_share','lagged':'remote_share+patents_per_100_eng_2020','full_pre':'remote_share+'+pre,'full+collab':'remote_share+collab_index_2023+'+pre,
'size_age':'remote_share+log_engineers_2020+firm_age_2020+C(region)+C(segment)+listed'}
for k,v in specs.items():
    m=smf.ols(y+'~'+v,d).fit(cov_type='HC1');print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
m=smf.ols(y+'~remote_share+'+pre,d).fit(cov_type='HC1');print(m.summary())
print(smf.ols('collab_index_2023~remote_share+'+pre,d).fit().params['remote_share'])
