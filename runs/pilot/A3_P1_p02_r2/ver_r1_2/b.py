import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
print(d.describe().T)
print(d.corr(numeric_only=True).round(2).to_string())
m=smf.ols(y+'~remote_share+'+pre,d).fit(cov_type='HC1')
print(m.summary())
nl=pre+'+I(log_engineers_2020**2)+I(firm_age_2020**2)+I(patents_per_100_eng_2020**2)+I(share_phd_2020**2)+I(cloud_spend_2020**2)'
m=smf.ols(y+'~remote_share+'+nl,d).fit(cov_type='HC1')
print('nl',m.params['remote_share'],m.bse['remote_share'])
m=smf.ols('collab_index_2023~remote_share+'+y+'+'+pre,d).fit()
print(m.params[:5])
