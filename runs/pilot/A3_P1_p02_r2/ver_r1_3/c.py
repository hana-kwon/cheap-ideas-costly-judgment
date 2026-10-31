import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
nl=pre+'+I(log_engineers_2020**2)+I(firm_age_2020**2)+I(patents_per_100_eng_2020**2)+log_engineers_2020:firm_age_2020+log_engineers_2020:patents_per_100_eng_2020+firm_age_2020:patents_per_100_eng_2020+I(log_engineers_2020**3)+I(firm_age_2020**3)'
for f in [pre,nl]:
    m=smf.ols(y+'~remote_share+'+f,d).fit(cov_type='HC1');print(m.params['remote_share'],m.bse['remote_share'])
for r,g in d.groupby('region'):
    m=smf.ols(y+'~remote_share+'+pre.replace('+C(region)',''),g).fit(cov_type='HC1');print(r,m.params['remote_share'],m.bse['remote_share'])
