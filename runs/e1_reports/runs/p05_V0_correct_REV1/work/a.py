import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
y="patents_per_100_eng_2023"
base="remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
pre="+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
for f in [y+"~remote_share",y+"~"+base,y+"~"+base+pre,y+"~"+base+pre+"+C(region)+listed+C(segment)",y+"~"+base+pre+"+collab_index_2023"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(f[-60:],r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
print(df[['remote_share','vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020']].corr().round(2))
r=smf.ols(y+"~"+base+pre,df).fit();print(r.summary().tables[1])
