import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
y='patents_per_100_eng_2023'
base="remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020"
full=base+"+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
lo,hi=df[y].quantile([.01,.99]); t=df[(df[y]>=lo)&(df[y]<=hi)]
for n,d in [('all',df),('trim',t)]:
    for k,f in [('base',base),('full',full)]:
        r=smf.ols(y+'~'+f,d).fit(cov_type='HC1')
        print(n,k,r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
