import pandas as pd, statsmodels.formula.api as smf, numpy as np
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
m=smf.ols(f'{y}~remote_share+{pre}',d).fit(cov_type='HC1');print(m.summary().tables[1])
print(d.describe().T)
print(d[['remote_share',y,'collab_index_2023']].corr())
print(smf.ols(f'collab_index_2023~remote_share+{y}+{pre}',d).fit().summary().tables[1])
for g,s in d.groupby('segment'):
    print(g,smf.ols(f'{y}~remote_share+{pre}',s).fit(cov_type='HC1').params['remote_share'])
for g,s in d.groupby('region'):
    print(g,smf.ols(f'{y}~remote_share+{pre}',s).fit(cov_type='HC1').params['remote_share'])
print(smf.ols(f'remote_share~{pre}',d).fit().summary().tables[1])
