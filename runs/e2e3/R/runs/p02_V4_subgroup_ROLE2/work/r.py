import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum(), df.region.value_counts().to_dict())
c="log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
allc=c+"+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(segment)"
for name,d in [("all",df)]+[(r,df[df.region==r]) for r in ['north','central','south']]:
    for f in ["patents_per_100_eng_2023~remote_share","patents_per_100_eng_2023~remote_share+"+c,"patents_per_100_eng_2023~remote_share+"+allc+("+C(region)" if name=="all" else "")]:
        m=smf.ols(f,d).fit(cov_type="HC1")
        print(name,len(d),f[-12:],round(m.params['remote_share'],3),round(m.bse['remote_share'],3),round(m.pvalues['remote_share'],4))
print(df.describe().T)
