import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.corr(numeric_only=True).round(2))
y='patents_per_100_eng_2023 ~ remote_share'
base=' + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020'
pre=base+' + vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)'
for n,f in [('raw',y),('base',y+base),('base+collab',y+base+'+collab_index_2023'),('pre',y+pre),('pre+collab',y+pre+'+collab_index_2023')]:
    m=smf.ols(f,d).fit(cov_type='HC1');print(n,m.params['remote_share'],m.bse['remote_share'])
