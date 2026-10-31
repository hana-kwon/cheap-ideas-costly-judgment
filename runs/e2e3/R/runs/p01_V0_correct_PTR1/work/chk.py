import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020"
full=f+"+C(region)+C(sector)+listed+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
y=df.productivity_2023;lo,hi=y.quantile([.01,.99]);t=df[(y>=lo)&(y<=hi)]
for n,d,ff in [("notrim",df,f),("trim",t,f),("full notrim",df,full),("full trim",t,full)]:
    r=smf.ols(ff,d).fit(cov_type="HC1");print(n,r.params["training_hours"],r.bse["training_hours"],r.pvalues["training_hours"])
print(df.isna().sum().sum())
