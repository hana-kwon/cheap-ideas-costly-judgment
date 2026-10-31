import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum())
base="patents_per_100_eng_2023 ~ remote_share"
c=" + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020"
c2=c+" + vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(segment)+C(region)"
for n,f,d in [("raw",base,df),("c",base+c,df),("c2",base+c2,df)]+[(r,base+c,df[df.region==r]) for r in ['north','central','south']]+[("c2n",base+c2,df[df.region=='north'])]:
    m=smf.ols(f,d).fit(cov_type="HC1");print(n,len(d),m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
print(df[['remote_share','vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020','log_engineers_2020','patents_per_100_eng_2020']].corr().round(2).iloc[0])
