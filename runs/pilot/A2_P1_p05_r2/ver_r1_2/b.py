import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv');y='patents_per_100_eng_2023'
cv=['log_engineers_2020','firm_age_2020','patents_per_100_eng_2020','vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020','listed','C(region)','C(segment)']
for c in cv:
    m=smf.ols(y+'~remote_share+'+'+'.join(x for x in cv if x!=c),d).fit(cov_type='HC1');print('drop',c,round(m.params['remote_share'],3),round(m.pvalues['remote_share'],3))
for c in cv:
    m=smf.ols('remote_share~'+c,d).fit();print(c,round(m.f_pvalue,4))
