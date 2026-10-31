import pandas as pd, statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum().sum())
y=df.productivity_2023
d=df[(y>=y.quantile(.01))&(y<=y.quantile(.99))]
for name,dd in [("trim",d),("all",df)]:
  for f in ["productivity_2023 ~ training_hours",
          "productivity_2023 ~ training_hours+log_employees_2020+firm_age_2020",
          "productivity_2023 ~ training_hours+log_employees_2020+firm_age_2020+productivity_2020",
          "productivity_2023 ~ training_hours+log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+listed+C(sector)+C(region)"]:
    r=smf.ols(f,dd).fit(cov_type="HC1")
    print(name,len(dd),f[-40:],r.params['training_hours'],r.bse['training_hours'],r.pvalues['training_hours'])
print(df[['training_hours','productivity_2020','productivity_2023']].corr())
