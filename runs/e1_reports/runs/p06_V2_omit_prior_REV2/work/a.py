import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum().sum())
for f in ["export_growth_2023~supplier_diversity",
"export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020",
"export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)",
"export_growth_2023~supplier_diversity*C(product_group)+log_sales_2020",
"export_growth_2023~supplier_diversity*C(region)+log_sales_2020",
"export_growth_2023~supplier_diversity*listed+log_sales_2020",
"export_growth_2023~supplier_diversity+buyer_rating_2023",
]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(f);print(r.summary().tables[1])
print(df.corr(numeric_only=True)['supplier_diversity'])
