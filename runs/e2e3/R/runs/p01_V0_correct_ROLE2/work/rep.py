import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df0 = pd.read_csv("data.csv")
print(df0.describe().T)
print(df0.isna().sum())
pre = ['log_employees_2020','firm_age_2020','productivity_2020']
allpre = pre+['export_share_2020','foreign_owned','family_owned','rd_intensity_2020','union_share_2020','credit_score_2020']
def run(name, d, rhs):
    f = smf.ols("productivity_2023 ~ "+rhs, d).fit(cov_type="HC1")
    print(f"{name}: {f.params['training_hours']:.3f} se {f.bse['training_hours']:.3f} p {f.pvalues['training_hours']:.4f} n {int(f.nobs)}")
y=df0.productivity_2023
lo,hi=y.quantile([.01,.99])
tr=df0[(y>=lo)&(y<=hi)]
run("raw",df0,"training_hours")
run("raw trim",tr,"training_hours")
run("pre3 notrim",df0,"training_hours+"+"+".join(pre))
run("pre3 trim",tr,"training_hours+"+"+".join(pre))
run("allpre notrim",df0,"training_hours+"+"+".join(allpre))
run("allpre trim",tr,"training_hours+"+"+".join(allpre))
run("allpre+cat notrim",df0,"training_hours+"+"+".join(allpre)+"+C(region)+C(sector)+listed")
run("allpre+cat trim",tr,"training_hours+"+"+".join(allpre)+"+C(region)+C(sector)+listed")
run("with mgmt (bad ctrl)",df0,"training_hours+mgmt_rating_2023+"+"+".join(allpre))
print(df0[['training_hours']+allpre+['productivity_2023','mgmt_rating_2023']].corr().round(2))
for q in [0.005,0.025,0.05]:
    lo,hi=y.quantile([q,1-q]); run(f"trim{q}",df0[(y>=lo)&(y<=hi)],"training_hours+"+"+".join(allpre))
