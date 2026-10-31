import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
m=smf.ols(f'{y}~remote_share+{pre}',d).fit(cov_type='HC1');print(m.summary())
print(d.corr(numeric_only=True).round(2))
for v in ['vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020']:
    print(v, smf.ols(f'{y}~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+{v}',d).fit().params['remote_share'])
