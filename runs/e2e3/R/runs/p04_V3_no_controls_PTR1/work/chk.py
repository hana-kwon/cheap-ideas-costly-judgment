import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
for f in ["productivity_2023~training_hours","productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(r.params["training_hours"],r.bse["training_hours"])
print(smf.ols("training_hours~log_employees_2020+firm_age_2020+productivity_2020",df).fit().summary().tables[1])
