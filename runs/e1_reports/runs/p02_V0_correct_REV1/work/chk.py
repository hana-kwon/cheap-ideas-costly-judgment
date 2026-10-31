import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
print(df.corr(numeric_only=True)['remote_share'])
base="patents_per_100_eng_2023 ~ remote_share"
pre="+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
allc=pre+"+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)"
for n,f in [("raw",base),("pre",base+pre),("all",base+allc)]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(n,r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
lo,hi=df.patents_per_100_eng_2023.quantile([.01,.99])
d=df[(df.patents_per_100_eng_2023>=lo)&(df.patents_per_100_eng_2023<=hi)]
r=smf.ols(base+allc,d).fit(cov_type="HC1");print('trim all',r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
print(r.summary())
