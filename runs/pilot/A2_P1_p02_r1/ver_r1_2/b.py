import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
for k in ['','+I(log_engineers_2020**2)+I(firm_age_2020**2)+I(patents_per_100_eng_2020**2)+log_engineers_2020:firm_age_2020']:
    m=smf.ols(f'{y}~remote_share+{pre}{k}',d).fit(cov_type='HC1');print(m.params['remote_share'],m.bse['remote_share'])
for s in ['hardware','software']:
    m=smf.ols(f'{y}~remote_share+{pre}',d[d.segment==s]).fit(cov_type='HC1');print(s,m.params['remote_share'],m.bse['remote_share'])
print(smf.ols(f'collab_index_2023~{pre}',d).fit().rsquared)
print(d[['collab_index_2023','remote_share']].corr())
m=smf.ols(f'{y}~remote_share+collab_index_2023+{pre}',d).fit();print(m.params[['remote_share','collab_index_2023']])
