import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)'
m=smf.ols(y+'~remote_share+'+pre,d).fit(cov_type='HC1');print(m.summary())
m=smf.ols('remote_share~'+pre,d).fit();print(m.rsquared, m.params, m.pvalues)
