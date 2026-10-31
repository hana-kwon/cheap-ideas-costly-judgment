import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
f="export_growth_2023 ~ supplier_diversity + log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
for e in ["", "+supplier_diversity:C(product_group)","+supplier_diversity:C(region)","+supplier_diversity:listed"]:
    m=smf.ols(f+e,d).fit(cov_type='HC1');print(m.summary().tables[1])
