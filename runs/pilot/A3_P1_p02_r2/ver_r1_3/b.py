import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
print(d.describe().T[['mean','std','min','max']])
print(d.drop(columns=['region','segment']).corr().round(2).to_string())
pre=['log_engineers_2020','firm_age_2020','patents_per_100_eng_2020','listed','vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020']
for c in pre:
    m=smf.ols(f'{y}~remote_share+{c}',d).fit(cov_type='HC1');print(c,m.params['remote_share'].round(3))
    m=smf.ols(f'remote_share~{c}',d).fit();print('  rs~',m.params[c].round(3),m.pvalues[c].round(4))
m=smf.ols(f'{y}~remote_share+collab_index_2023+'+'+'.join(pre),d).fit();print(m.params[['remote_share','collab_index_2023']])
m=smf.ols(f'collab_index_2023~{y}+'+'+'.join(pre),d).fit();print(m.params[y])
m=smf.ols(f'collab_index_2023~remote_share+{y}+'+'+'.join(pre),d).fit();print(m.params[['remote_share',y]])
