import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.corr(numeric_only=True).round(2))
y='patents_per_100_eng_2023'
allpre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
for f in ['remote_share+'+allpre,'remote_share+'+allpre+'+collab_index_2023']:
    m=smf.ols(y+'~'+f,d).fit(cov_type='HC1');print(m.params['remote_share'],m.bse['remote_share'])
print(smf.ols('collab_index_2023~remote_share+'+allpre,d).fit().summary().tables[1])
print(smf.ols('collab_index_2023~'+y+'+remote_share',d).fit().params)
