import pandas as pd, numpy as np
import statsmodels.api as sm

df = pd.read_csv("data.csv")
print(df.shape)
print(df.isna().sum())
print(df.describe().T)

def fit(cols, d, label):
    d = d.dropna(subset=cols + ["productivity_2023"])
    X = sm.add_constant(d[cols].astype(float))
    r = sm.OLS(d["productivity_2023"].astype(float), X).fit(cov_type="HC1")
    print(f"{label}: n={len(d)} b={r.params['training_hours']:.4f} se={r.bse['training_hours']:.4f} p={r.pvalues['training_hours']:.4g}")

y = df["productivity_2023"]
lo, hi = y.quantile([0.01, 0.99])
t = df[(y >= lo) & (y <= hi)]

base = ['training_hours', 'log_employees_2020', 'firm_age_2020', 'productivity_2020']
fit(base, df, "report-spec untrimmed")
fit(base, t, "report-spec trimmed")
fit(['training_hours'], df, "bivariate untrimmed")
fit(['training_hours', 'productivity_2020'], df, "with pre outcome only")
pre = ['export_share_2020', 'foreign_owned', 'family_owned', 'rd_intensity_2020', 'union_share_2020', 'credit_score_2020']
fit(base + pre, df, "full pre-period controls")
fit(base + pre + ['listed'], df, "full + listed")
fit(base + ['mgmt_rating_2023'], df, "with mgmt rating (post)")

# correlation of training_hours with pre-period covariates
num = df.select_dtypes(include=[np.number]).columns
print(df[num].corr()["training_hours"].sort_values())
