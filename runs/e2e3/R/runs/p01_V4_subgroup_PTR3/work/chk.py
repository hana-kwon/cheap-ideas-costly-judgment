import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
for name,d in [("all",df),("north",df[df.region=="north"]),("central",df[df.region=="central"]),("south",df[df.region=="south"])]:
    g=f if name=="all" else f.replace("+C(region)","")
    r=smf.ols(g,d).fit(cov_type="HC1")
    print(name,len(d),r.params["training_hours"],r.bse["training_hours"],r.pvalues["training_hours"])
n=df[df.region=="north"]
r=smf.ols("productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020",n).fit(cov_type="HC1")
print("north untrimmed minimal",r.params["training_hours"],r.bse["training_hours"])
