import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
for f in ['patents_per_100_eng_2023 ~ remote_share','patents_per_100_eng_2023 ~ remote_share+log_engineers_2020+firm_age_2020',
'patents_per_100_eng_2023 ~ remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020',
'patents_per_100_eng_2023 ~ remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)']:
    m=smf.ols(f,d).fit(cov_type='HC1');print(m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
print(d.corr(numeric_only=True)['remote_share'])
