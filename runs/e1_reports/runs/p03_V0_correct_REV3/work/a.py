import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum())
base='export_growth_2023 ~ supplier_diversity'
pre=' + log_sales_2020+years_exporting_2020+export_growth_2020'
allp=pre+'+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)'
for n,f in [('none',base),('rep',base+pre),('all',base+allp)]:
    r=smf.ols(f,df).fit(cov_type='HC1');print(n,r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
print(smf.ols(base+allp,df).fit(cov_type='HC1').summary())
print(df.corr(numeric_only=True)['supplier_diversity'])
