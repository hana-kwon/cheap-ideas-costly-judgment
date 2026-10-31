import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
print(d.describe().T)
for f in [y+'~remote_share', y+'~remote_share+patents_per_100_eng_2020+log_engineers_2020+firm_age_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020']:
  for dd in [d, d[d[y].between(*d[y].quantile([.01,.99]))]]:
    r=smf.ols(f,dd).fit(cov_type='HC1');print(r.params['remote_share'],r.bse['remote_share'])
print(d.corr(numeric_only=True)['remote_share'])
