import pandas as pd, statsmodels.formula.api as smf, numpy as np
df=pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum().sum())
base="export_growth_2023~supplier_diversity"
allc="log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"
for f in [base,
base+"+log_sales_2020+years_exporting_2020+export_growth_2020",
base+"+"+allc,
base+"+I(supplier_diversity**2)+"+allc,
base+"+buyer_rating_2023+"+allc,
"export_growth_2023~supplier_diversity*C(product_group)+supplier_diversity*C(region)+supplier_diversity*listed+supplier_diversity*foreign_owned+"+allc]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(f);print(r.summary().tables[1])
print(df.corr(numeric_only=True)['supplier_diversity'])
print(df.corr(numeric_only=True)['export_growth_2023'])
