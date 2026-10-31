import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre=['log_sales_2020','years_exporting_2020','export_growth_2020']
allp=pre+['inventory_days_2020','foreign_owned','share_imported_inputs_2020','port_distance_km','certified_iso','debt_ratio_2020']
for f in ['supplier_diversity','supplier_diversity+'+'+'.join(pre),'supplier_diversity+'+'+'.join(allp),'supplier_diversity+'+'+'.join(allp)+'+C(region)+listed+C(product_group)']:
    r=smf.ols('export_growth_2023~'+f,df).fit(cov_type='HC1');print(r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
print(df.corr(numeric_only=True)['supplier_diversity'])
print(df.isna().sum().sum())
