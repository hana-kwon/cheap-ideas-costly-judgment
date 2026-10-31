import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
base="patents_per_100_eng_2023 ~ remote_share"
c=" + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020"
allc=c+" + C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
for name,d in [("all",df)]+[(r,df[df.region==r]) for r in ["north","central","south"]]:
    for f in [base,base+c,base+allc]:
        if name!="all": f=f.replace(" + C(region)","")
        m=smf.ols(f,d).fit(cov_type="HC1")
        print(name,len(d),f[-20:],round(m.params['remote_share'],3),round(m.bse['remote_share'],3),round(m.pvalues['remote_share'],4))
print(df[['remote_share','collab_index_2023','patents_per_100_eng_2023']].corr())
print(smf.ols("remote_share ~ log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)",df).fit().summary().tables[1])
