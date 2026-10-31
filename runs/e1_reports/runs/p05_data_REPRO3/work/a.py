import pandas as pd,statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
allp=pre+'+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
S={'raw':'',
'pre3':'+'+pre,
'allpre':'+'+allp,
'allpre+collab':'+'+allp+'+collab_index_2023',
'size_only':'+log_engineers_2020',
'lagged_only':'+patents_per_100_eng_2020',
}
for k,v in S.items():
    r=smf.ols(y+'~remote_share'+v,d).fit(cov_type='HC1')
    print(k,round(r.params['remote_share'],4),round(r.bse['remote_share'],4),r.pvalues['remote_share'])
r=smf.ols(y+'~remote_share*C(segment)+'+allp,d).fit(cov_type='HC1');print(r.params.filter(like='remote'),r.pvalues.filter(like='remote'))
r=smf.ols(y+'~remote_share+I(remote_share**2)+'+allp,d).fit(cov_type='HC1');print(r.params.filter(like='remote'),r.pvalues.filter(like='remote'))
r=smf.ols(y+'~remote_share+'+allp,d[d.remote_share.abs()<3]).fit(cov_type='HC1');print('trim',r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
