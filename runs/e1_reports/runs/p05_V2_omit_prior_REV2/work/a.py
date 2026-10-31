import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
for f in ['patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020',
 'patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020',
 'patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)',
 'remote_share~patents_per_100_eng_2020+log_engineers_2020+firm_age_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020']:
    r=smf.ols(f,d).fit(cov_type='HC1');print(r.summary().tables[1])
