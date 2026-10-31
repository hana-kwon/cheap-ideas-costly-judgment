import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.describe().T)
print(df.corr(numeric_only=True)['training_hours'])
y=df.productivity_2023
lo,hi=y.quantile([.01,.99])
t=df[(y>=lo)&(y<=hi)]
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+listed+C(sector)"
for name,d in [("trim",t),("all",df)]:
    for f in ["productivity_2023~training_hours",
              "productivity_2023~training_hours+log_employees_2020+firm_age_2020",
              "productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020",
              "productivity_2023~training_hours+"+pre]:
        r=smf.ols(f,d).fit(cov_type="HC1")
        print(name,len(d),f[-40:],round(r.params['training_hours'],3),round(r.bse['training_hours'],3),round(r.pvalues['training_hours'],4))
