import pandas as pd, numpy as np, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.patents_per_100_eng_2023.describe())
print(df.patents_per_100_eng_2023.quantile([.01,.05,.5,.95,.99]))
print((df.patents_per_100_eng_2023>=df.patents_per_100_eng_2023.max()-1e-9).sum())
b="+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
for f in ["patents_per_100_eng_2023~remote_share","patents_per_100_eng_2023~remote_share"+b,
 "patents_per_100_eng_2023~remote_share*C(segment)"+b,"patents_per_100_eng_2023~remote_share*listed"+b,
 "patents_per_100_eng_2023~remote_share*C(region)"+b,
 "patents_per_100_eng_2023~remote_share+I(remote_share**2)"+b]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(f);print(r.summary().tables[1])
