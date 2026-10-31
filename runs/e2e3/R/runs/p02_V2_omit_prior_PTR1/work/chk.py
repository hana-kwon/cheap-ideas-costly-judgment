import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
y="patents_per_100_eng_2023"
for name,d in [("all",df),("trim",df[(df[y]>=df[y].quantile(.01))&(df[y]<=df[y].quantile(.99))])]:
    for f in ["remote_share+log_engineers_2020+firm_age_2020","remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"]:
        r=smf.ols(y+"~"+f,d).fit(cov_type="HC1")
        print(name,len(d),f[-20:],r.params["remote_share"],r.bse["remote_share"])
print(df[y].describe())
