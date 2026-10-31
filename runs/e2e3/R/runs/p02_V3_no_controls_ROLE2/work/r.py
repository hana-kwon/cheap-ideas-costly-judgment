import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum(), df.remote_share.describe())
c="log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
for f in ["patents_per_100_eng_2023~remote_share","patents_per_100_eng_2023~remote_share+"+c,"patents_per_100_eng_2023~remote_share+"+c+"+collab_index_2023"]:
    m=smf.ols(f,df).fit(cov_type="HC1");print(m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
print(smf.ols("remote_share~"+c,df).fit().summary().tables[1])
