import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
allc='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
m=smf.ols(f'{y}~remote_share+'+allc,d).fit(cov_type='HC3');print(m.summary().tables[1])
m=smf.ols(f'{y}~remote_share+I(remote_share**2)+'+allc,d).fit(cov_type='HC3');print(m.params[['remote_share','I(remote_share ** 2)']],m.pvalues[['remote_share','I(remote_share ** 2)']])
for c in ['C(segment)','C(region)','listed']:
    m=smf.ols(f'{y}~remote_share*{c}+'+allc,d).fit(cov_type='HC3');print(m.pvalues.filter(like='remote_share:'))
m=smf.ols(f'remote_share~'+allc,d).fit();print(m.rsquared, m.pvalues[m.pvalues<.01])
