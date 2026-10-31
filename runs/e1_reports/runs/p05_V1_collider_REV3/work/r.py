import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
pre2=pre+'+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)'
for f in [y+'~remote_share',y+'~remote_share+'+pre,y+'~remote_share+'+pre2,y+'~remote_share+'+pre+'+collab_index_2023','collab_index_2023~remote_share+'+pre]:
    m=smf.ols(f,d).fit(cov_type='HC1');print(f[-40:],m.params['remote_share'],m.bse['remote_share'])
print(d[['remote_share','collab_index_2023',y]].corr())
