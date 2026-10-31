import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
y="patents_per_100_eng_2023"
pre="log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
full=pre+"+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(segment)+C(region)"
for name,d in [("all",df)]+[(r,g) for r,g in df.groupby("region")]:
  for f in ["1",pre,full]:
    m=smf.ols(f"{y}~remote_share+{f}",d).fit(cov_type="HC1")
    print(name,len(d),f[:10],round(m.params.remote_share,3),round(m.bse.remote_share,3),round(m.pvalues.remote_share,4))
print(df.isna().sum().sum()); print(df.groupby("region").remote_share.describe())
print(df[["remote_share","vc_backed","founder_ceo","cloud_spend_2020","hq_in_hub_city","share_phd_2020","gross_margin_2020","patents_per_100_eng_2020"]].corr().round(2).iloc[0])
