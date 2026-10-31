import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
y="patents_per_100_eng_2023"
print(df[y].describe())
base=y+"~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
pre=base+"+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)"
for n,f in [("base",base),("pre",pre),("raw",y+"~remote_share")]:
    for d,l in [(df,"full"),(df[(df[y]>=df[y].quantile(.01))&(df[y]<=df[y].quantile(.99))],"trim")]:
        r=smf.ols(f,d).fit(cov_type="HC1");print(n,l,len(d),r.params["remote_share"],r.bse["remote_share"],r.pvalues["remote_share"])
