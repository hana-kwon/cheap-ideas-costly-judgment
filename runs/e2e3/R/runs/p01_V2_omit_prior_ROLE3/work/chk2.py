import pandas as pd, statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
base="productivity_2023 ~ training_hours+log_employees_2020+firm_age_2020+productivity_2020+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020+listed+C(sector)+C(region)"
for extra in ["", "+I(training_hours**2)", "+training_hours:C(sector)", "+training_hours:C(region)","+mgmt_rating_2023","+I(productivity_2020**2)+productivity_2020:training_hours"]:
    r=smf.ols(base+extra,df).fit(cov_type="HC1")
    print(extra, r.params.filter(like='training').round(3).to_dict(), r.pvalues.filter(like='training').round(4).to_dict())
print(df.training_hours.describe())
