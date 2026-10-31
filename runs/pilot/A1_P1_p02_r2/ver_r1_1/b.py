import pandas as pd, numpy as np, statsmodels.formula.api as smf
pd.set_option('display.width',250)
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
print(d.describe().T)
print(d.corr(numeric_only=True).round(2).to_string())
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
m=smf.ols(y+'~remote_share+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
d2=d[(d[y]>d[y].quantile(.01))&(d[y]<d[y].quantile(.99))]
print(smf.ols(y+'~remote_share+'+pre,d2).fit(cov_type='HC1').params['remote_share'])
m=smf.ols(y+'~remote_share+I(remote_share**2)+'+pre,d).fit(cov_type='HC1');print(m.params.iloc[-13:],m.pvalues.iloc[-3:])
