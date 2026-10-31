import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
f='patents_per_100_eng_2023 ~ remote_share + log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
for r in ['north','central','south']:
    m=smf.ols(f,d[d.region==r]).fit(cov_type='HC1')
    print(r,m.nobs,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
m=smf.ols(f+'+C(region)',d).fit(cov_type='HC1')
print('all',m.params['remote_share'],m.bse['remote_share'])
