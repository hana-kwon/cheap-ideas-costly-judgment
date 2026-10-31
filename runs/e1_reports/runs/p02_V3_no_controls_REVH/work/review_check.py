import pandas as pd, numpy as np
import statsmodels.api as sm
df = pd.read_csv("data.csv")
y = df["patents_per_100_eng_2023"]
lo, hi = y.quantile([0.01, 0.99])
d = df[(y >= lo) & (y <= hi)].copy()

def fit(cols, data, label):
    X = sm.add_constant(data[cols].astype(float))
    r = sm.OLS(data["patents_per_100_eng_2023"], X, missing="drop").fit(cov_type="HC1")
    print(label, "n=", int(r.nobs), "b=", round(r.params["remote_share"], 3),
          "se=", round(r.bse["remote_share"], 3), "p=", round(r.pvalues["remote_share"], 4))

fit(["remote_share"], df, "raw untrimmed")
fit(["remote_share"], d, "raw trimmed")
ctrl = ["log_engineers_2020","firm_age_2020","patents_per_100_eng_2020","listed","vc_backed",
        "founder_ceo","cloud_spend_2020","hq_in_hub_city","share_phd_2020","gross_margin_2020"]
fit(["remote_share"]+ctrl, d, "with pre controls")
fit(["remote_share","patents_per_100_eng_2020"], d, "with lagged outcome")
d2 = pd.get_dummies(d, columns=["region","segment"], drop_first=True, dtype=float)
extra = [c for c in d2.columns if c.startswith("region_") or c.startswith("segment_")]
fit(["remote_share"]+ctrl+extra, d2, "controls+FE")
print("corr remote vs lagged outcome", np.corrcoef(d["remote_share"], d["patents_per_100_eng_2020"])[0,1])
print("corr remote vs log_eng", np.corrcoef(d["remote_share"], d["log_engineers_2020"])[0,1])
print("corr remote vs hub", np.corrcoef(d["remote_share"], d["hq_in_hub_city"])[0,1])
print(d.groupby(pd.qcut(d["remote_share"],5))[["patents_per_100_eng_2023","patents_per_100_eng_2020"]].mean())
