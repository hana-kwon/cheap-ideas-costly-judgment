import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020"
for r in ['north','central','south']:
    d=df[df.region==r]; m=smf.ols(f,d).fit(cov_type="HC1"); print(r,len(d),m.params['supplier_diversity'],m.bse['supplier_diversity'])
m=smf.ols(f,df).fit(cov_type="HC1");print('all',m.params['supplier_diversity'],m.bse['supplier_diversity'])
m=smf.ols(f+"*C(region)",df).fit(cov_type="HC1");print(m.summary().tables[1])
