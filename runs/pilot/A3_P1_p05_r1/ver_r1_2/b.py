import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
y='patents_per_100_eng_2023'
print(smf.ols(f'{y}~remote_share+{pre}',d).fit(cov_type='HC3').summary().tables[1])
print(d.corr(numeric_only=True).round(2).to_string())
print(smf.ols(f'collab_index_2023~remote_share+{y}+{pre}',d).fit().summary().tables[1])
