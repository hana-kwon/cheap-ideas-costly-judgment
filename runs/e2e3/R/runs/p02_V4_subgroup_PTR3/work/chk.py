import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
m=smf.ols(f,df).fit(cov_type="HC1");print(m.params['remote_share'],m.bse['remote_share'])
for r,d in df.groupby('region'):
    g=f.replace("+C(region)","")
    m=smf.ols(g,d).fit(cov_type="HC1");print(r,len(d),m.params['remote_share'],m.bse['remote_share'])
m=smf.ols(f+"+remote_share:C(region)",df).fit(cov_type="HC1");print(m.summary().tables[1])
