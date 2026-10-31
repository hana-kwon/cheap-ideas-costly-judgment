import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum(), df.describe().T[['min','max']])
y=df.export_growth_2023
lo,hi=y.quantile([.01,.99]);t=df[(y>=lo)&(y<=hi)]
base='export_growth_2023~supplier_diversity'
pre=' + log_sales_2020+years_exporting_2020+export_growth_2020'
allp=pre+' + inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)'
for n,d in [('full',df),('trim',t)]:
  for k,f in [('none',base),('pre',base+pre),('allpre',base+allp),('post',base+pre+'+buyer_rating_2023')]:
    m=smf.ols(f,d).fit(cov_type='HC1');print(n,k,round(m.params['supplier_diversity'],3),round(m.bse['supplier_diversity'],3),round(m.pvalues['supplier_diversity'],4))
print(df[['supplier_diversity','buyer_rating_2023','export_growth_2023','export_growth_2020']].corr())
