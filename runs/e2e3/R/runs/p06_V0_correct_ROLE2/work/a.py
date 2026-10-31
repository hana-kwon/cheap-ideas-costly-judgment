import pandas as pd, numpy as np, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T[['count','mean','std','min','max']])
base="export_growth_2023 ~ supplier_diversity"
c1=" + log_sales_2020+years_exporting_2020+export_growth_2020"
c2=c1+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"
lo,hi=df.export_growth_2023.quantile([.01,.99])
t=df[(df.export_growth_2023>=lo)&(df.export_growth_2023<=hi)]
for n,d in [('all',df),('trim',t)]:
  for f in [base,base+c1,base+c2]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(n,len(d),f[-30:],r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
r=smf.ols(base+c2+"+buyer_rating_2023",df).fit(cov_type="HC1");print(r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
print(df.isna().sum().sum())
for g,d in df.groupby('product_group'):
    r=smf.ols(base+c1,d).fit(cov_type="HC1");print(g,r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
for g,d in df.groupby('region'):
    r=smf.ols(base+c1,d).fit(cov_type="HC1");print(g,r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
for g,d in df.groupby('listed'):
    r=smf.ols(base+c1,d).fit(cov_type="HC1");print(g,r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
