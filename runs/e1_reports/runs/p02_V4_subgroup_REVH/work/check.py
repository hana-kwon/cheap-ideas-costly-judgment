import pandas as pd, numpy as np
import statsmodels.formula.api as smf

d = pd.read_csv("data.csv")
y = "patents_per_100_eng_2023"

def fit(df, f, label):
    lo, hi = df[y].quantile([0.01, 0.99])
    s = df[(df[y] >= lo) & (df[y] <= hi)]
    m = smf.ols(f, data=s).fit(cov_type="HC1")
    print(f"{label:45s} n={int(m.nobs)} b={m.params['remote_share']:.3f} se={m.bse['remote_share']:.3f} p={m.pvalues['remote_share']:.3f}")

base = "patents_per_100_eng_2023 ~ remote_share + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020"
fit(d[d.region=="north"], base, "north, preferred")
fit(d, base, "full sample, same controls")
fit(d, base + " + C(region)", "full sample + region FE")
fit(d, base + " + C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+collab_index_2023", "full + region FE + all covariates")
for r in ["central", "south"]:
    fit(d[d.region==r], base, f"{r} only")
fit(d[d.region=="north"], base + "+ listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020", "north, all pre-period covariates")
fit(d[d.region=="north"], "patents_per_100_eng_2023 ~ remote_share", "north, bivariate")
print(d.groupby("region")[["remote_share", y]].agg(["mean","std"]))
