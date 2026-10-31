import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
base="patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
for f in ["patents_per_100_eng_2023~remote_share",base,base+"+collab_index_2023",
"collab_index_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020",
base+"+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)"]:
    m=smf.ols(f,d).fit(cov_type='HC1');print(f,m.params['remote_share'],m.bse['remote_share'])
