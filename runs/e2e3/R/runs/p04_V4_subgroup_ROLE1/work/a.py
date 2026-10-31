import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+listed"
for name,d in [("all",df),("north",df[df.region=="north"]),("central",df[df.region=="central"]),("south",df[df.region=="south"])]:
  for f in ["productivity_2023~training_hours","productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020","productivity_2023~training_hours+"+pre, "productivity_2023~training_hours+C(region)+"+pre]:
    if name!="all" and "C(region)" in f: continue
    r=smf.ols(f,d).fit(cov_type="HC1");print(name,len(d),f[-12:],round(r.params["training_hours"],3),round(r.bse["training_hours"],3),round(r.pvalues["training_hours"],4))
