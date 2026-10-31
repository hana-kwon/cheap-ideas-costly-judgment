import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
y="patents_per_100_eng_2023"
b="~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
ex="+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)"
lo,hi=df[y].quantile([.01,.99]);t=df[(df[y]>=lo)&(df[y]<=hi)]
for n,d in [("full",df),("trim",t)]:
  for k,f in [("base",y+b),("ex",y+b+ex),("none",y+"~remote_share")]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(n,k,len(d),r.params["remote_share"],r.bse["remote_share"],r.pvalues["remote_share"])
print(df[y].describe()); print(df.isna().sum().sum())
