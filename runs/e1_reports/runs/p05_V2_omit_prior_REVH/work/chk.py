import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.remote_share.std(), d[['remote_share','patents_per_100_eng_2023']].corr())
y=d.patents_per_100_eng_2023
d2=d[(y>=y.quantile(.01))&(y<=y.quantile(.99))].copy()
specs={
'base':'patents_per_100_eng_2023 ~ remote_share + log_engineers_2020 + firm_age_2020',
'+lag':'patents_per_100_eng_2023 ~ remote_share + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020',
'+all':'patents_per_100_eng_2023 ~ remote_share + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020 + collab_index_2023 + C(region) + listed + C(segment) + vc_backed + founder_ceo + cloud_spend_2020 + hq_in_hub_city + share_phd_2020 + gross_margin_2020',
}
for k,f in specs.items():
    for nm,dd in [('trim',d2),('full',d)]:
        r=smf.ols(f,dd).fit(cov_type='HC1')
        print(k,nm,len(dd),round(r.params['remote_share'],3),round(r.bse['remote_share'],3),round(r.pvalues['remote_share'],4))
r=smf.ols('patents_per_100_eng_2023 ~ remote_share',d).fit(cov_type='HC1'); print('bivariate',r.params['remote_share'],r.pvalues['remote_share'])
r=smf.ols('patents_per_100_eng_2020 ~ remote_share',d).fit(cov_type='HC1'); print('pre outcome',r.params['remote_share'],r.pvalues['remote_share'])
r=smf.ols('collab_index_2023 ~ remote_share',d).fit(cov_type='HC1'); print('collab',r.params['remote_share'],r.pvalues['remote_share'])
d['rs_bin']=pd.qcut(d.remote_share,4,labels=False)
print(d.groupby('rs_bin').patents_per_100_eng_2023.agg(['mean','median','count']))
