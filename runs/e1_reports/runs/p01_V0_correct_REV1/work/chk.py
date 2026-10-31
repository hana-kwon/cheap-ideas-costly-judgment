import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
pre="log_employees_2020+firm_age_2020+productivity_2020"
allp=pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+C(sector)+listed"
for name,f in [("naive","productivity_2023~training_hours"),("report","productivity_2023~training_hours+"+pre),("allpre","productivity_2023~training_hours+"+allp),("withmgmt","productivity_2023~training_hours+mgmt_rating_2023+"+allp)]:
    for d,l in [(df,"all"),(df[(df.productivity_2023>=df.productivity_2023.quantile(.01))&(df.productivity_2023<=df.productivity_2023.quantile(.99))],"trim")]:
        r=smf.ols(f,d).fit(cov_type="HC1")
        print(name,l,r.params["training_hours"],r.bse["training_hours"],r.pvalues["training_hours"],int(r.nobs))
print(df.corr(numeric_only=True)["training_hours"])
