import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020"
for r in ['north','central','south',None]:
    d=df if r is None else df[df.region==r]
    m=smf.ols(f,d).fit(cov_type="HC1"); print(r,len(d),m.params['supplier_diversity'],m.bse['supplier_diversity'],m.pvalues['supplier_diversity'])
m=smf.ols(f+"+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020",df).fit(cov_type="HC1");print(m.params['supplier_diversity'],m.bse['supplier_diversity'])
print(smf.ols("export_growth_2023~supplier_diversity",df).fit(cov_type="HC1").summary().tables[1])
