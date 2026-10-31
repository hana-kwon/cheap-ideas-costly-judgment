import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
c="log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
y="patents_per_100_eng_2023"
lo,hi=df[y].quantile([.01,.99]);t=df[(df[y]>=lo)&(df[y]<=hi)]
for n,d in [("all",df),("trim",t)]:
    m=smf.ols(y+"~remote_share+"+c,d).fit(cov_type="HC1");print(n,m.params['remote_share'],m.bse['remote_share'])
for k in ["log_engineers_2020","firm_age_2020","patents_per_100_eng_2020"]:
    m=smf.ols(y+"~remote_share+"+k,df).fit(cov_type="HC1");print(k,m.params['remote_share'],m.bse['remote_share'])
m=smf.ols(y+"~remote_share*log_engineers_2020+remote_share*firm_age_2020+"+c+"+I(remote_share**2)",df).fit(cov_type="HC1");print(m.summary().tables[1])
print(df[y].describe())
