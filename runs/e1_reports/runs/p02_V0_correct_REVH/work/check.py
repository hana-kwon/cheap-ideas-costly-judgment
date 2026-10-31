import pandas as pd, numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm

df = pd.read_csv("data.csv")
print(df.shape)
print(df.describe().T.to_string())
print(df.isna().sum().to_string())

y = df["patents_per_100_eng_2023"]
lo, hi = y.quantile([0.01, 0.99])
d = df[(y >= lo) & (y <= hi)].dropna(subset=["remote_share","patents_per_100_eng_2023","log_engineers_2020","firm_age_2020","patents_per_100_eng_2020"])
print("trimmed n", len(d))

def run(f, data, label):
    m = smf.ols(f, data=data).fit(cov_type="HC1")
    print(label, "coef=%.4f se=%.4f p=%.4f" % (m.params["remote_share"], m.bse["remote_share"], m.pvalues["remote_share"]))

base = "patents_per_100_eng_2023 ~ remote_share + log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020"
run(base, d, "base trimmed")
run(base, df, "base untrimmed")
run("patents_per_100_eng_2023 ~ remote_share", df, "bivariate untrimmed")
run("patents_per_100_eng_2023 ~ remote_share + log_engineers_2020 + firm_age_2020", df, "no lagged DV")
full = base + " + vc_backed + founder_ceo + cloud_spend_2020 + hq_in_hub_city + share_phd_2020 + gross_margin_2020 + listed + C(region) + C(segment)"
run(full, d, "full controls trimmed")
run(full, df, "full controls untrimmed")
run(base + " + C(region) + C(segment)", d, "base+FE")
# Pre-period balance: does remote_share correlate with pre-period covariates?
for c in ["vc_backed","founder_ceo","cloud_spend_2020","hq_in_hub_city","share_phd_2020","gross_margin_2020","log_engineers_2020","firm_age_2020","patents_per_100_eng_2020","listed"]:
    m = smf.ols(f"remote_share ~ {c}", data=df).fit(cov_type="HC1")
    print("balance", c, "coef=%.4f p=%.4f" % (m.params[c], m.pvalues[c]))
# Check for outcome: pre-period lag coefficient
m = smf.ols("patents_per_100_eng_2023 ~ patents_per_100_eng_2020", data=df).fit()
print("lag only r2", m.rsquared)
