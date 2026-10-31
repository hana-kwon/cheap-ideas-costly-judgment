import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(segment)+C(region)"
for name,d in [("all",df),("central",df[df.region=="central"])]:
  for f in ["patents_per_100_eng_2023~remote_share","patents_per_100_eng_2023~remote_share+"+pre]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(name,len(d),r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
for g,d in df.groupby("region"):
    r=smf.ols("patents_per_100_eng_2023~remote_share+"+pre.replace("+C(region)",""),d).fit(cov_type="HC1");print(g,len(d),r.params['remote_share'],r.bse['remote_share'])
print(df.describe().T)
