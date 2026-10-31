import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
df=df.rename(columns={'patents_per_100_eng_2023':'y','patents_per_100_eng_2020':'p0'})
print(df.isna().sum().sum())
for f in ['y~remote_share','y~remote_share+log_engineers_2020+firm_age_2020+p0',
 'y~remote_share+log_engineers_2020+firm_age_2020+p0+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)']:
    r=smf.ols(f,df).fit(cov_type='HC1');print(f,r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
print(df.corr(numeric_only=True)['remote_share'])
print(df.corr(numeric_only=True)['y'])
