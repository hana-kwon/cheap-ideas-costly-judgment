import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
b='patents_per_100_eng_2023 ~ remote_share + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020'
pre=' + vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)'
for n,f in [('base',b),('+collab',b+'+collab_index_2023'),('pre',b+pre),('pre+collab',b+pre+'+collab_index_2023'),('raw','patents_per_100_eng_2023 ~ remote_share')]:
    r=smf.ols(f,df).fit(cov_type='HC1');print(n,r.params['remote_share'],r.bse['remote_share'])
print(smf.ols('collab_index_2023 ~ remote_share',df).fit().params)
print(df.corr(numeric_only=True)['remote_share'])
