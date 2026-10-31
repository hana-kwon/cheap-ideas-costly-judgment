import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.describe().T)
print(df.corr(numeric_only=True)['remote_share'])
y='patents_per_100_eng_2023'
def f(form,d=df):
    r=smf.ols(form,d).fit(cov_type='HC1'); print(form, r.params['remote_share'], r.bse['remote_share'], r.nobs)
f(y+'~remote_share')
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
f(y+'~remote_share+'+pre)
f(y+'~remote_share+patents_per_100_eng_2020')
f(y+'~remote_share+'+pre+'+collab_index_2023')
f(y+'~remote_share+C(segment)+C(region)+listed+log_engineers_2020')
