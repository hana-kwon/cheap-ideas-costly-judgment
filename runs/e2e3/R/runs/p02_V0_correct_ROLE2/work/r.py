import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T[['count','mean','std','min','max']])
y='patents_per_100_eng_2023'
pre=' + vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020'
base='remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
lo,hi=df[y].quantile([.01,.99]); t=df[(df[y]>=lo)&(df[y]<=hi)]
for n,f,d in [('orig',base,t),('notrim',base,df),('none',' remote_share',df),('pre',base+pre,df),('pre trim',base+pre,t),('pre+cat',base+pre+'+C(region)+listed+C(segment)',df),('collab',base+pre+'+collab_index_2023',df)]:
    r=smf.ols(y+'~'+f,d).fit(cov_type='HC1'); print(n,len(d),r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
print(df[['remote_share','vc_backed','founder_ceo','cloud_spend_2020','hq_in_hub_city','share_phd_2020','gross_margin_2020','log_engineers_2020','firm_age_2020','patents_per_100_eng_2020',y]].corr().round(2)[['remote_share',y]])
