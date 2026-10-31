import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum().sum())
print(df.corr(numeric_only=True)['training_hours'])
def f(form, d=df):
    r = smf.ols(form, d).fit(cov_type="HC1")
    print(form[:120], round(r.params['training_hours'],3), round(r.bse['training_hours'],3), round(r.pvalues['training_hours'],4), int(r.nobs))
base='productivity_2023 ~ training_hours'
f(base)
pre='+log_employees_2020+firm_age_2020+productivity_2020'
f(base+pre)
y=df.productivity_2023; lo,hi=y.quantile([.01,.99])
t=df[(y>=lo)&(y<=hi)]
f(base+pre,t)
allpre=pre+'+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+C(sector)+listed'
f(base+allpre)
f(base+allpre,t)
f(base+allpre+'+mgmt_rating_2023')
for s in ['manufacturing','services']:
    f(base+allpre, df[df.sector==s])
f('np.log(productivity_2023) ~ training_hours'+allpre) if (df.productivity_2023>0).all() else print('nonpos')
f(base+allpre+'+I(training_hours**2)')
