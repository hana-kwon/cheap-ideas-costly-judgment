import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020"
for n,d in [("full",df)]+[(r,g) for r,g in df.groupby("region")]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(n,len(d),r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
r=smf.ols(f+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)",df).fit(cov_type="HC1");print(r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
