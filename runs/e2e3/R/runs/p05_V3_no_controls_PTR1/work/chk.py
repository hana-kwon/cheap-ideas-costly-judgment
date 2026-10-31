import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
for f in ["patents_per_100_eng_2023~remote_share","patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
print(df[['remote_share','log_engineers_2020','firm_age_2020','patents_per_100_eng_2020']].corr().round(2))
