import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
pre="log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)"
y="patents_per_100_eng_2023"
specs={
'raw':f"{y}~remote_share",
'lagged':f"{y}~remote_share+patents_per_100_eng_2020",
'full_pre':f"{y}~remote_share+{pre}",
'full_pre+collab(mediator)':f"{y}~remote_share+{pre}+collab_index_2023",
'full_pre_quad':f"{y}~remote_share+I(remote_share**2)+{pre}",
'full_pre_interact_segment':f"{y}~remote_share*C(segment)+{pre}",
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC3')
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],m.rsquared)
m=smf.ols(specs['full_pre'],d).fit(cov_type='HC3');print(m.summary())
print(d[['remote_share','collab_index_2023',y]].corr())
d['lp']=np.log(d[y]);m=smf.ols(f"lp~remote_share+{pre}",d).fit(cov_type='HC3');print('log',m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
