import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("data.csv")
y = df["patents_per_100_eng_2023"]
lo, hi = y.quantile([0.01, 0.99])
num = df.drop(columns=["region", "segment"])
d = num[(y >= lo) & (y <= hi)].astype(float)

def fit(cols, data):
    X = sm.add_constant(data[cols])
    r = sm.OLS(data["patents_per_100_eng_2023"], X).fit(cov_type="HC1")
    return round(r.params["remote_share"], 3), round(r.bse["remote_share"], 3), round(r.pvalues["remote_share"], 4), int(r.nobs)

base = ['log_engineers_2020', 'firm_age_2020', 'patents_per_100_eng_2020']
print("full (report spec, trimmed):", fit(['remote_share'] + base + ['collab_index_2023'], d))
print("without collab (trimmed):   ", fit(['remote_share'] + base, d))
print("untrimmed, no collab:       ", fit(['remote_share'] + base, num.astype(float)))
print("untrimmed, with collab:      ", fit(['remote_share'] + base + ['collab_index_2023'], num.astype(float)))

# Is collab downstream of remote work?
print("corr(remote_share, collab_index_2023):", round(d["remote_share"].corr(d["collab_index_2023"]), 3))
r = sm.OLS(d["collab_index_2023"], sm.add_constant(d[['remote_share'] + base])).fit(cov_type="HC1")
print("collab ~ remote_share + base: coef", round(r.params["remote_share"], 3), "p", round(r.pvalues["remote_share"], 4))
r2 = sm.OLS(d["patents_per_100_eng_2023"], sm.add_constant(d[['collab_index_2023', 'remote_share'] + base])).fit(cov_type="HC1")
print("collab coef in outcome model:", round(r2.params["collab_index_2023"], 3))
