import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum().sum())
for f in ["export_growth_2023~supplier_diversity","export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020",
"export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
print(df.corr(numeric_only=True)['supplier_diversity'])
for g,d in df.groupby('product_group'):
    r=smf.ols("export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+share_imported_inputs_2020+port_distance_km+debt_ratio_2020",d).fit(cov_type="HC1");print(g,r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
