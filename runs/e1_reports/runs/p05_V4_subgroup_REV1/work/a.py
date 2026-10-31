import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum(), df.remote_share.describe())
f="patents_per_100_eng_2023 ~ remote_share"
c=" + log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
c2=c+"+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)"
for n,d in [("all",df)]+[(r,df[df.region==r]) for r in df.region.unique()]:
  for k,ff in [("none",f),("c",f+c),("c2",f+c2)]:
    if n!="all": ff=ff.replace("+C(region)","")
    m=smf.ols(ff,d).fit(cov_type="HC1");print(n,k,round(m.params['remote_share'],3),round(m.bse['remote_share'],3),round(m.pvalues['remote_share'],4),len(d))
print(smf.ols("remote_share ~ log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)",df).fit().summary().tables[1])
