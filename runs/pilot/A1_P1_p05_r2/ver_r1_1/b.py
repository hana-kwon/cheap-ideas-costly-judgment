import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
nl=pre+'+I(log_engineers_2020**2)+I(firm_age_2020**2)+I(patents_per_100_eng_2020**2)+log_engineers_2020:firm_age_2020+log_engineers_2020:patents_per_100_eng_2020+firm_age_2020:patents_per_100_eng_2020'
m=smf.ols(f'{y}~remote_share+{nl}',d).fit(cov_type='HC1');print(m.params['remote_share'],m.pvalues['remote_share'])
for c in ['region','segment','listed']:
    m=smf.ols(f'{y}~remote_share*C({c})+{pre}',d).fit(cov_type='HC1');print(m.params.filter(like='remote'),m.pvalues.filter(like='remote'))
# collab as mediator vs collider: corr of collab with pre-period y
print(d[['collab_index_2023','patents_per_100_eng_2020','remote_share',y]].corr())
