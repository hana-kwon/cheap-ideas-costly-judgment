import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.region.value_counts())
c='supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020'
for name,d in [('all',df)]+[(r,df[df.region==r]) for r in ['north','central','south']]:
    for f in ['export_growth_2023~supplier_diversity','export_growth_2023~'+c, 'export_growth_2023~'+c+'+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+listed+C(product_group)+C(region)']:
        r=smf.ols(f,d).fit(cov_type='HC1');print(name,len(d),round(r.params['supplier_diversity'],3),round(r.bse['supplier_diversity'],3),round(r.pvalues['supplier_diversity'],4))
