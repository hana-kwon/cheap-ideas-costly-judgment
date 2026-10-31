import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
for name,f,s in [('naive',y+'~remote_share',d),
 ('full',y+'~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020',d),
 ('basic',y+'~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020',d),
 ('central',y+'~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020',d[d.region=='central'])]:
    r=smf.ols(f,s).fit(cov_type='HC1');print(name,len(s),r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
for g,s in d.groupby('region'):
    r=smf.ols(y+'~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020',s).fit(cov_type='HC1');print(g,len(s),r.params['remote_share'],r.pvalues['remote_share'])
print(d.corr(numeric_only=True)['remote_share'])
print(d.isna().sum().sum(), d.region.value_counts())
