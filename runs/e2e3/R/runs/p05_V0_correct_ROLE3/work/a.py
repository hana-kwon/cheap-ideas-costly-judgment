import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pd.set_option("display.width",200)
print(df[['remote_share','patents_per_100_eng_2020','log_engineers_2020','firm_age_2020','collab_index_2023','patents_per_100_eng_2023']].corr().round(3))
print(df.patents_per_100_eng_2023.describe())
b="patents_per_100_eng_2023 ~ remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
for f in [b, b+"+I(remote_share**2)", b+"+collab_index_2023", b+"+C(segment)*remote_share", b+"+C(region)*remote_share+listed*remote_share"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(f);print(r.summary().tables[1])
