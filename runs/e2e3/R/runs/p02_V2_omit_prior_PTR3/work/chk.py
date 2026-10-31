import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
lo,hi=d[y].quantile([.01,.99]);t=d[(d[y]>=lo)&(d[y]<=hi)]
for nm,dd in [('all',d),('trim',t)]:
    for k,f in [('analyst','remote_share+log_engineers_2020+firm_age_2020'),('full','remote_share+'+pre)]:
        m=smf.ols(y+'~'+f,dd).fit(cov_type='HC1');print(nm,k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
