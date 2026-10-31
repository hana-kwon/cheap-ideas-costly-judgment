import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
print(d.isna().sum().sum(), d.describe().T[['mean','std','min','max']])
allpre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
m=smf.ols(y+'~remote_share+'+allpre,d).fit(cov_type='HC1');print(m.summary().tables[1])
print(smf.ols('collab_index_2023~remote_share+'+allpre,d).fit().summary().tables[1])
print(smf.ols('collab_index_2023~'+y+'+remote_share+'+allpre,d).fit().params[[y,'remote_share']])
print(d[['remote_share',y,'collab_index_2023']].corr())
for s in ['hardware','software']:
  print(s,smf.ols(y+'~remote_share+'+allpre,d[d.segment==s]).fit(cov_type='HC1').params['remote_share'])
