import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre=["log_employees_2020","firm_age_2020","productivity_2020","C(region)","listed","C(sector)","export_share_2020","foreign_owned","family_owned","rd_intensity_2020","union_share_2020","credit_score_2020"]
for c in pre:
    r=smf.ols("productivity_2023~training_hours+"+c,df).fit(cov_type="HC1");print(c,round(r.params['training_hours'],3))
y=df.productivity_2023;lo,hi=y.quantile([.01,.99]);d=df[(y>=lo)&(y<=hi)]
r=smf.ols("productivity_2023~training_hours+"+"+".join(pre),d).fit(cov_type="HC1");print("trim+pre",r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
