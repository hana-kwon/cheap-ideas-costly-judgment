import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum())
y='patents_per_100_eng_2023'
def run(f,d=df):
    r=smf.ols(f,d).fit(cov_type="HC1")
    print(f[:150]); print(' remote',r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'],int(r.nobs))
base=f"{y} ~ remote_share"
run(base)
run(base+"+log_engineers_2020+firm_age_2020")
run(base+"+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020")
pre="+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)"
run(base+pre)
lo,hi=df[y].quantile([.01,.99])
d2=df[(df[y]>=lo)&(df[y]<=hi)]
run(base+pre,d2)
run(base+pre+"+collab_index_2023")
print(df[['remote_share',y,'patents_per_100_eng_2020','collab_index_2023','log_engineers_2020','cloud_spend_2020','hq_in_hub_city']].corr().round(2))
