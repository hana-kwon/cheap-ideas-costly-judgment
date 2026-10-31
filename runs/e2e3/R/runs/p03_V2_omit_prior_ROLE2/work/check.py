import pandas as pd, numpy as np
import statsmodels.formula.api as smf
df = pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum().sum())
print(df.corr(numeric_only=True)['supplier_diversity'])
base='export_growth_2023 ~ supplier_diversity'
pre=' + log_sales_2020 + years_exporting_2020'
allc=pre+' + export_growth_2020 + inventory_days_2020 + foreign_owned + share_imported_inputs_2020 + port_distance_km + certified_iso + debt_ratio_2020 + listed + C(region) + C(product_group)'
y=df.export_growth_2023
lo,hi=y.quantile([.01,.99])
t=df[(y>=lo)&(y<=hi)]
for name,f,d in [('raw',base,df),('analyst',base+pre,t),('analyst untrimmed',base+pre,df),
  ('prior growth',base+pre+' + export_growth_2020',df),('prior growth trimmed',base+pre+' + export_growth_2020',t),
  ('all',base+allc,df),('all trimmed',base+allc,t)]:
    r=smf.ols(f,d).fit(cov_type='HC1')
    print(name,len(d),r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
r=smf.ols(base+allc,df).fit(cov_type='HC1');print(r.summary())
