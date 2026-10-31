import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(open('analysis.py').read())
c='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
c2=c+'+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)'
for n,f,s in [('full',c,d),('full2',c2,d),('north',c,d[d.region=='north']),('nocontrol',"1",d)]:
    m=smf.ols('patents_per_100_eng_2023~remote_share+'+f,s).fit(cov_type='HC1')
    print(n,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],len(s))
for r in ['north','central','south']:
    s=d[d.region==r]
    m=smf.ols('patents_per_100_eng_2023~remote_share+'+c2.replace('+C(region)',''),s).fit(cov_type='HC1')
    print(r,m.params['remote_share'],m.bse['remote_share'],len(s))
