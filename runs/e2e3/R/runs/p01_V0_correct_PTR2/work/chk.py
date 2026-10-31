import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
base="productivity_2023 ~ training_hours + log_employees_2020 + firm_age_2020 + productivity_2020"
full=base+" + export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+C(sector)+listed"
y=df.productivity_2023;lo,hi=y.quantile([.01,.99]);t=df[(y>=lo)&(y<=hi)]
for n,f,d in [("an-notrim",base,df),("an-trim",base,t),("full-notrim",full,df),("full-trim",full,t)]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(n,r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
