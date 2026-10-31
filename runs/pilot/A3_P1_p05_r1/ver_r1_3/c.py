import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
y='patents_per_100_eng_2023'
for g,s in d.groupby('founder_ceo'):
    m=smf.ols(f'{y}~remote_share+{pre}',s).fit(cov_type='HC3');print(g,len(s),m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
m=smf.ols(f'{y}~remote_share*founder_ceo+{pre}',d).fit(cov_type='HC3');print(m.params.filter(like='remote'),m.pvalues.filter(like='remote'))
for v in ['hq_in_hub_city','listed']:
  for g,s in d.groupby(v):
    m=smf.ols(f'{y}~remote_share+{pre.replace("+"+v,"").replace(v+"+","")}',s).fit(cov_type='HC3');print(v,g,len(s),m.params['remote_share'],m.bse['remote_share'])
