import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
df=df.rename(columns={'patents_per_100_eng_2023':'y','patents_per_100_eng_2020':'p0'})
f='y~remote_share+log_engineers_2020+firm_age_2020+p0'
for r,d in [('all',df)]+list(df.groupby('region')):
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(r,len(d),m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
m=smf.ols(f+'*C(region)',df).fit(cov_type='HC1')
m=smf.ols(f+'+remote_share:C(region)',df).fit(cov_type='HC1');print(m.params.filter(like='remote'),m.pvalues.filter(like='remote'))
