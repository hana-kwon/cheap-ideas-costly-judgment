import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
y='patents_per_100_eng_2023'
print(df[y].std())
pre="+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)"
for v in ['C(segment)','C(region)','listed','hq_in_hub_city','vc_backed']:
    r=smf.ols(f"{y}~remote_share*{v}"+pre,df).fit(cov_type="HC1")
    print(v,r.params.filter(like='remote').round(2).to_dict(),r.pvalues.filter(like='remote').round(3).to_dict())
r=smf.ols(f"{y}~remote_share+I(remote_share**2)"+pre,df).fit(cov_type="HC1")
print(r.params.filter(like='remote'),r.pvalues.filter(like='remote'))
r=smf.ols(f"np.log({y})~remote_share"+pre,df).fit(cov_type="HC1")
print(r.params['remote_share'],r.pvalues['remote_share'])
