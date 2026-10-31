import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
print(df.region.value_counts())
base="patents_per_100_eng_2023~remote_share"
pre="+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
allc=pre+"+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
for name,d in [("all",df)]+[(r,df[df.region==r]) for r in df.region.unique()]:
    for f in [base,base+pre,base+allc]:
        if name!="all": f=f.replace("+C(region)","")
        r=smf.ols(f,d).fit(cov_type="HC1")
        print(name,len(d),f[-12:],round(r.params['remote_share'],3),round(r.bse['remote_share'],3),round(r.pvalues['remote_share'],4))
print(df.corr(numeric_only=True)['remote_share'])
