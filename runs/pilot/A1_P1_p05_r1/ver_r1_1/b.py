import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y="patents_per_100_eng_2023"
print(d.corr(numeric_only=True).round(2).to_string())
cs=["log_engineers_2020","firm_age_2020","patents_per_100_eng_2020","vc_backed","founder_ceo","cloud_spend_2020","hq_in_hub_city","share_phd_2020","gross_margin_2020","C(region)","listed","C(segment)"]
for c in cs:
    m=smf.ols(f"{y}~remote_share+{c}",d).fit(cov_type='HC3');print(c,m.params['remote_share'],m.bse['remote_share'])
m=smf.ols(f"{y}~remote_share+"+"+".join(cs),d).fit(cov_type='HC3');print(m.summary())
