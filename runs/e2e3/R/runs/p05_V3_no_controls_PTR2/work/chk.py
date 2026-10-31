import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="patents_per_100_eng_2023 ~ remote_share + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020 + vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)"
r=smf.ols(f,df).fit(cov_type="HC3");print(r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
print(smf.ols("remote_share ~ log_engineers_2020 + firm_age_2020",df).fit().rsquared)
