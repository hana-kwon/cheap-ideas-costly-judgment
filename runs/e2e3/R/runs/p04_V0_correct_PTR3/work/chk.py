import pandas as pd, statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
a = smf.ols("productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020", df).fit(cov_type="HC1")
print(a.params["training_hours"], a.bse["training_hours"])
b = smf.ols("productivity_2023~training_hours+log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020", df).fit(cov_type="HC1")
print(b.params["training_hours"], b.bse["training_hours"])
