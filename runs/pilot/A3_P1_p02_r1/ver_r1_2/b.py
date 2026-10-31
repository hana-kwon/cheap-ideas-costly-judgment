import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.corr(numeric_only=True).round(2).to_string())
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
y='patents_per_100_eng_2023'
m=smf.ols(y+'~remote_share+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
m=smf.ols('remote_share~'+pre,d).fit();print(m.summary().tables[1])
m=smf.ols(y+'~remote_share+I(remote_share**2)+'+pre,d).fit(cov_type='HC1');print(m.params[['remote_share','I(remote_share ** 2)']],m.pvalues[['remote_share','I(remote_share ** 2)']])
for s,g in d.groupby('segment'):
    print(s,smf.ols(y+'~remote_share+'+pre.replace('+C(segment)',''),g).fit(cov_type='HC1').params['remote_share'])
