import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
f="export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
m=smf.ols(f,d).fit(cov_type='HC1');print(m.summary().tables[1])
print(smf.ols(f+"+I(supplier_diversity**2)",d).fit(cov_type='HC1').summary().tables[1])
print(d.corr(numeric_only=True).round(2).to_string())
print(smf.ols(f+"+buyer_rating_2023",d).fit(cov_type='HC1').params['supplier_diversity'])
