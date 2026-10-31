import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
r=smf.ols(f,df).fit(cov_type="HC1");print(r.params['remote_share'],r.bse['remote_share'])
for g,d in df.groupby('region'):
    f2=f.replace("+C(region)","")
    r=smf.ols(f2,d).fit(cov_type="HC1");print(g,len(d),r.params['remote_share'],r.bse['remote_share'])
d=df[df.region=='north']
r=smf.ols(f.replace("+C(region)",""),d).fit(cov_type="HC1");print(r.params['remote_share'],r.bse['remote_share'])
