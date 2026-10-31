import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
def f(s,dd=d):
    m=smf.ols(s,dd).fit(cov_type='HC1');print(s[-60:],round(m.params['remote_share'],3),round(m.bse['remote_share'],3),m.pvalues['remote_share'],int(m.nobs))
y='patents_per_100_eng_2023~remote_share'
f(y)
f(y+'+log_engineers_2020+firm_age_2020')
f(y+'+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020')
pre='+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)'
f(y+pre)
f(y+pre+'+collab_index_2023')
lo,hi=d.patents_per_100_eng_2023.quantile([.01,.99])
f(y+pre,d[(d.patents_per_100_eng_2023>=lo)&(d.patents_per_100_eng_2023<=hi)])
print(d.corr(numeric_only=True)['remote_share'])
print(d.isna().sum().sum())
