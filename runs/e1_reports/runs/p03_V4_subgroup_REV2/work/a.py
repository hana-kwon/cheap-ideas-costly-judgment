import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
c=' + log_sales_2020+years_exporting_2020+export_growth_2020'
for name,d in [('all',df)]+[(r,g) for r,g in df.groupby('region')]:
    for f in ['export_growth_2023 ~ supplier_diversity','export_growth_2023 ~ supplier_diversity'+c]:
        r=smf.ols(f,d).fit(cov_type='HC1'); print(name,len(d),f[-20:],round(r.params['supplier_diversity'],3),round(r.bse['supplier_diversity'],3),round(r.pvalues['supplier_diversity'],4))
f='export_growth_2023 ~ supplier_diversity'+c+'+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)'
r=smf.ols(f,df).fit(cov_type='HC1');print(r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
print(df.isna().sum().sum(), df.groupby('region').size())
