import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.isna().sum().sum(), len(df))
pre = "log_employees_2020+firm_age_2020+productivity_2020"
full = pre+"+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+C(region)+C(sector)+listed"
for name, f in [("none","productivity_2023~training_hours"),
                ("pre","productivity_2023~training_hours+"+pre),
                ("full pre","productivity_2023~training_hours+"+full),
                ("analyst","productivity_2023~training_hours+"+pre+"+mgmt_rating_2023"),
                ("full+mgmt","productivity_2023~training_hours+"+full+"+mgmt_rating_2023")]:
    r = smf.ols(f, df).fit(cov_type="HC1")
    print(name, r.params["training_hours"], r.bse["training_hours"], r.pvalues["training_hours"])
print(smf.ols("mgmt_rating_2023~training_hours+"+pre, df).fit().summary().tables[1])
print(smf.ols("mgmt_rating_2023~productivity_2023+training_hours+"+pre, df).fit().params)
print(df[["training_hours","productivity_2023","mgmt_rating_2023"]].corr())
