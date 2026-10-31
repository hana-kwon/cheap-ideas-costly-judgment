import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+listed+C(product_group)"
for r in ['north','central','south']:
    d=df[df.region==r]
    m=smf.ols(f,d).fit(cov_type="HC1")
    print(r,len(d),m.params['supplier_diversity'],m.bse['supplier_diversity'])
m=smf.ols(f+"+C(region)",df).fit(cov_type="HC1");print('all',m.params['supplier_diversity'],m.bse['supplier_diversity'])
m=smf.ols(f+"+C(region)+supplier_diversity:C(region)",df).fit(cov_type="HC1");print(m.summary().tables[1])
