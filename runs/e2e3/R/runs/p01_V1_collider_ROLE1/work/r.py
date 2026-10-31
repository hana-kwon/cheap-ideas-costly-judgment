import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
y=df.productivity_2023;lo,hi=y.quantile([.01,.99]);d=df[(y>=lo)&(y<=hi)]
pre="log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(sector)+C(region)+listed"
for f in ["productivity_2023~training_hours","productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020+mgmt_rating_2023",
"productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020","productivity_2023~training_hours+"+pre,"productivity_2023~training_hours+mgmt_rating_2023+"+pre]:
  for dd in (d,df):
    r=smf.ols(f,dd).fit(cov_type="HC1");print(round(r.params['training_hours'],3),round(r.bse['training_hours'],3),len(dd))
print(df[['training_hours','mgmt_rating_2023','productivity_2023','productivity_2020']].corr())
