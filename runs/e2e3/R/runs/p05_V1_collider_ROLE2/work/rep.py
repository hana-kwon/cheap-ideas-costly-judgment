import pandas as pd, statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.describe().T[['count','mean','std']])
print(df.corr(numeric_only=True)['remote_share'])
base="patents_per_100_eng_2023 ~ remote_share"
pre=" + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020"
pre2=pre+" + vc_backed + founder_ceo + cloud_spend_2020 + hq_in_hub_city + share_phd_2020 + gross_margin_2020 + C(region)+listed+C(segment)"
for name,f in [("raw",base),("pre",base+pre),("pre+collab",base+pre+"+collab_index_2023"),("pre2",base+pre2),("pre2+collab",base+pre2+"+collab_index_2023")]:
    r=smf.ols(f,df).fit(cov_type="HC1")
    print(name,r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'],int(r.nobs))
r=smf.ols("collab_index_2023 ~ remote_share"+pre2,df).fit(cov_type="HC1")
print("collab on remote",r.params['remote_share'],r.pvalues['remote_share'])
