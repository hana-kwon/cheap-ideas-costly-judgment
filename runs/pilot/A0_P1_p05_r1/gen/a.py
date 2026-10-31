import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
y='patents_per_100_eng_2023'
pre='log_engineers_2020+firm_age_2020+patents_per_100_eng_2020'
chars='vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+listed+C(region)+C(segment)'
specs={
'1 raw':'remote_share',
'2 +size,age,lag patents':'remote_share+'+pre,
'3 +all pre-period (preferred)':'remote_share+'+pre+'+'+chars,
'4 +collab (post-treatment, mediator)':'remote_share+'+pre+'+'+chars+'+collab_index_2023',
'5 no lag outcome, all chars':'remote_share+log_engineers_2020+firm_age_2020+'+chars,
'6 quadratic':'remote_share+I(remote_share**2)+'+pre+'+'+chars,
}
n=0
for k,f in specs.items():
    m=smf.ols(y+'~'+f,d).fit(cov_type='HC1'); n+=1
    print(k,m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'],m.nobs)
m=smf.ols(y+'~remote_share*segment+'+pre+'+'+chars,d).fit(cov_type='HC1');print(m.summary().tables[1]);n+=1
# collab as outcome
m=smf.ols('collab_index_2023~remote_share+'+pre+'+'+chars,d).fit(cov_type='HC1');print('collab',m.params['remote_share'],m.bse['remote_share']);n+=1
# winsor/trim
q=d[y].quantile([.01,.99]);dt=d[(d[y]>q.iloc[0])&(d[y]<q.iloc[1])]
m=smf.ols(y+'~remote_share+'+pre+'+'+chars,dt).fit(cov_type='HC1');n+=1
print('trim',m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
m=smf.ols(f'np.log({y})~remote_share+'+pre+'+'+chars,d).fit(cov_type='HC1');n+=1
print('log y',m.params['remote_share'],m.bse['remote_share'],m.pvalues['remote_share'])
print(n)
print(smf.ols(y+'~remote_share+'+pre+'+'+chars,d).fit(cov_type='HC1').summary().tables[1])
