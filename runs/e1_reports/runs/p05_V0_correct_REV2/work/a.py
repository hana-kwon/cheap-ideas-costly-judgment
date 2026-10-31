import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
b="patents_per_100_eng_2023 ~ remote_share + log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
for extra in ["","+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)","+collab_index_2023"]:
    f=smf.ols(b+extra,df).fit(cov_type="HC1");print(extra,f.params['remote_share'],f.bse['remote_share'],f.pvalues['remote_share'])
print(df.corr(numeric_only=True)['remote_share'])
f=smf.ols("remote_share ~ vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020",df).fit();print(f.summary().tables[1])
