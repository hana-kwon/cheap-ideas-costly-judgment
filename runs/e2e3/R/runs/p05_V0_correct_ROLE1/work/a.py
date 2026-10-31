import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
y=df.patents_per_100_eng_2023
b="patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
pre="+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
t=df[(y>=y.quantile(.01))&(y<=y.quantile(.99))]
for name,f,d in [("orig",b,t),("pre",b+pre,t),("pre full",b+pre,df),("pre full+cat",b+pre+"+C(region)+listed+C(segment)",df),("none","patents_per_100_eng_2023~remote_share",df)]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(name,r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'],len(d))
print(df[['remote_share','vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020','patents_per_100_eng_2023']].corr().round(2))
