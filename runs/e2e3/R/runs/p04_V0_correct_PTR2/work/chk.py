import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
c="log_employees_2020+firm_age_2020+productivity_2020"
full=c+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for n,f,d in [("analyst-notrim",c,df),("full",full,df),("analyst-sub",c,df)]:
    r=smf.ols("productivity_2023~training_hours+"+f,d).fit(cov_type="HC1")
    print(n,r.params["training_hours"],r.bse["training_hours"],len(d))
y=df.productivity_2023;lo,hi=y.quantile([.01,.99]);d=df[(y>=lo)&(y<=hi)]
for n,f in [("an-trim",c),("full-trim",full)]:
    r=smf.ols("productivity_2023~training_hours+"+f,d).fit(cov_type="HC1")
    print(n,r.params["training_hours"],r.bse["training_hours"],len(d))
print(df.isna().sum().sum())
