import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
for f in ['export_growth_2023~supplier_diversity+I(supplier_diversity**2)+'+pre,
 'export_growth_2023~supplier_diversity*C(product_group)+supplier_diversity*C(region)+'+pre,
 'export_growth_2023~supplier_diversity+'+pre+'+I(log_sales_2020**2)+I(export_growth_2020**2)+log_sales_2020:export_growth_2020']:
    m=smf.ols(f,d).fit(cov_type='HC1');print(m.summary().tables[1])
m=smf.ols('supplier_diversity~'+pre,d).fit();print(m.summary().tables[1])
