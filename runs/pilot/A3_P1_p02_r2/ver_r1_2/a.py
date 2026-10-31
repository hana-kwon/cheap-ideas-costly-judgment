import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
specs={
'raw':'remote_share',
'lagged_y':'remote_share+patents_per_100_eng_2020',
'size_age_lag':'remote_share+patents_per_100_eng_2020+log_engineers_2020+firm_age_2020',
'full_pre':'remote_share+'+pre,
'full_pre_plus_collab':'remote_share+collab_index_2023+'+pre,
'collab_only':'remote_share+collab_index_2023',
}
for k,v in specs.items():
    m=smf.ols(y+'~'+v,d).fit(cov_type='HC1')
    print(k,round(m.params['remote_share'],4),round(m.bse['remote_share'],4),m.pvalues['remote_share'],m.nobs)
m=smf.ols('collab_index_2023~remote_share+'+pre,d).fit(cov_type='HC1');print('collab on remote',m.params['remote_share'],m.pvalues['remote_share'])
m=smf.ols(y+'~remote_share*C(segment)+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
d['rs2']=d.remote_share**2
m=smf.ols(y+'~remote_share+rs2+'+pre,d).fit(cov_type='HC1');print(m.params[['remote_share','rs2']],m.pvalues[['remote_share','rs2']])
print(d[['remote_share']+[c for c in d.columns if c not in('region','segment','remote_share','firm_id')]].corr()['remote_share'])
