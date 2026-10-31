import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
oth='+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
cat='+C(region)+listed+C(segment)'
S={'raw':'',
'pre3':'+'+pre,
'pre3+cat':'+'+pre+cat,
'full pre':'+'+pre+cat+oth,
'full+collab':'+'+pre+cat+oth+'+collab_index_2023',
'collab only':'+collab_index_2023',
'no lagged outcome':'+log_engineers_2020+firm_age_2020'+cat+oth}
for k,v in S.items():
    m=smf.ols('patents_per_100_eng_2023~remote_share'+v,d).fit(cov_type='HC1')
    print(k,round(m.params['remote_share'],3),round(m.bse['remote_share'],3),m.pvalues['remote_share'],m.nobs)
