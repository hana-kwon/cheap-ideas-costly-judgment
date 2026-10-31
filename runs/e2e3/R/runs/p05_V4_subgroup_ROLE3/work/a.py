import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="patents_per_100_eng_2023 ~ remote_share"
c=" + log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
c2=c+"+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(segment)+C(region)"
for n,d in [("all",df)]+[(r,df[df.region==r]) for r in ['north','central','south']]:
    for fm in [f,f+c,f+c2]:
        m=smf.ols(fm,d).fit(cov_type="HC1"); print(n,len(d),m.params['remote_share'].round(3),m.bse['remote_share'].round(3),m.pvalues['remote_share'].round(4))
print(df.describe().T)
print(df[['remote_share','vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020','patents_per_100_eng_2023','patents_per_100_eng_2020']].corr().round(2))
