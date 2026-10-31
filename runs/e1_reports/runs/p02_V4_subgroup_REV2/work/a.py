import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum())
base="patents_per_100_eng_2023~remote_share"
c="+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
c2=c+"+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(segment)+listed"
for n,d in [("all",df)]+[(r,df[df.region==r]) for r in df.region.unique()]:
    for f in [base,base+c,base+c2+("+C(region)" if n=="all" else "")]:
        r=smf.ols(f,d).fit(cov_type="HC1")
        print(n,len(d),f[-20:],round(r.params['remote_share'],3),round(r.bse['remote_share'],3),round(r.pvalues['remote_share'],4))
print(df.groupby('region').remote_share.mean())
