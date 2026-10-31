import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum())
print(df.corr(numeric_only=True)['remote_share'])
y='patents_per_100_eng_2023'
def run(f, d=df, label=''):
    r = smf.ols(f, d).fit(cov_type='HC1')
    print(label, f[:90], round(r.params['remote_share'],3), round(r.bse['remote_share'],3), round(r.pvalues['remote_share'],4), int(r.nobs))
base='log_engineers_2020 + firm_age_2020 + patents_per_100_eng_2020'
run(f'{y}~remote_share')
run(f'{y}~remote_share+{base}')
lo,hi=df[y].quantile([.01,.99])
run(f'{y}~remote_share+{base}', df[(df[y]>=lo)&(df[y]<=hi)],'trim')
allc=base+'+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020+C(region)+listed+C(segment)'
run(f'{y}~remote_share+{allc}')
run(f'{y}~remote_share+{allc}', df[(df[y]>=lo)&(df[y]<=hi)],'trim')
for s in df.segment.unique():
    run(f'{y}~remote_share+{allc}', df[df.segment==s], s)
for s in df.region.unique():
    run(f'{y}~remote_share+{allc}', df[df.region==s], s)
run(f'{y}~remote_share+{allc}+collab_index_2023',label='collab')
print(df[y].describe())
df['ly']=np.log1p(df[y].clip(lower=0))
run(f'ly~remote_share+{allc}')
# which covariates predict remote
print(smf.ols(f'remote_share~{allc}',df).fit().summary().tables[1])
