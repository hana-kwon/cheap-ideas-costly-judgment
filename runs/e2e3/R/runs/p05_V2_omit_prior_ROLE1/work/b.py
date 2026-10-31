import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
for f in ["patents_per_100_eng_2023~remote_share",
"patents_per_100_eng_2023~remote_share+patents_per_100_eng_2020",
"patents_per_100_eng_2023~remote_share+log_engineers_2020",
"patents_per_100_eng_2023~remote_share+firm_age_2020",
"patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(f[-40:],r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
r=smf.ols("remote_share~log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)",df).fit()
print(r.summary().tables[1])
