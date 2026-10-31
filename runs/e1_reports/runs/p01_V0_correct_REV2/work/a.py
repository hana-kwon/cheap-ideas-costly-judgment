import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
lo,hi=df.productivity_2023.quantile([.01,.99])
pre="log_employees_2020+firm_age_2020+productivity_2020"
full=pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for name,d in [("trim",df[(df.productivity_2023>=lo)&(df.productivity_2023<=hi)]),("all",df)]:
  for f in ["1",pre,full]:
    r=smf.ols("productivity_2023~training_hours+"+f,d).fit(cov_type="HC1")
    print(name,f[:20],r.params.training_hours,r.bse.training_hours,r.pvalues.training_hours)
print(df.corr(numeric_only=True)["training_hours"])
