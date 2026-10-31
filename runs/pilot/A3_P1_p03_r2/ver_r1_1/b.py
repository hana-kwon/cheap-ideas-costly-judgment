import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
print(d.isna().sum().sum())
f='export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+listed+C(region)+C(product_group)'
for g in [f, f+'+buyer_rating_2023']:
    r=smf.ols(g,d).fit(cov_type='HC1');print(r.params['supplier_diversity'],r.bse['supplier_diversity'])
print(d.corr(numeric_only=True).round(2).to_string())
