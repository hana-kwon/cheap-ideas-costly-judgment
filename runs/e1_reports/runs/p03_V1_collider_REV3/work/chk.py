import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.corr(numeric_only=True).round(2)[['supplier_diversity','export_growth_2023','buyer_rating_2023']])
base='export_growth_2023 ~ supplier_diversity + log_sales_2020 + years_exporting_2020 + export_growth_2020'
for f in [base, base+'+buyer_rating_2023', 'export_growth_2023 ~ supplier_diversity', base+'+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)']:
    r=smf.ols(f,df).fit(cov_type='HC1'); print(r.params['supplier_diversity'],r.bse['supplier_diversity'])
print(smf.ols('buyer_rating_2023 ~ supplier_diversity + export_growth_2023',df).fit().summary().tables[1])
