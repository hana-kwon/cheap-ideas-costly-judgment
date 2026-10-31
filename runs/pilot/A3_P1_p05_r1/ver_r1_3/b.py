import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
y='patents_per_100_eng_2023'
print(d[y].std())
for extra in ['','+I(log_engineers_2020**2)+I(firm_age_2020**2)+I(patents_per_100_eng_2020**2)','+log_engineers_2020:firm_age_2020+log_engineers_2020:patents_per_100_eng_2020']:
    m=smf.ols(f'{y}~remote_share+{pre}{extra}',d).fit(cov_type='HC3');print(m.params['remote_share'],m.bse['remote_share'])
for v in ['region','listed','vc_backed','hq_in_hub_city','founder_ceo']:
    m=smf.ols(f'{y}~remote_share*C({v})+{pre}',d).fit(cov_type='HC3');print(v,m.pvalues.filter(like='remote_share:').values)
print(smf.ols(f'collab_index_2023~remote_share+{y}+{pre}',d).fit().summary().tables[1])
print(smf.ols(f'collab_index_2023~remote_share+{pre}',d).fit().params['remote_share'])
