import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
y='patents_per_100_eng_2023'
base='remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
ctrl=base+'+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)'
for name,df in [('full',d),('central',d[d.region=='central'])]:
  for f in [y+'~remote_share',y+'~'+base,y+'~'+ctrl]:
    m=smf.ols(f,df).fit(cov_type='HC1');print(name,f[:40],len(df),m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
