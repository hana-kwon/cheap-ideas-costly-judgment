import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum()); print(df.describe().T[['mean','std','min','max']])
base="export_growth_2023 ~ supplier_diversity"
pre="+log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"
for f in [base, base+"+log_sales_2020+years_exporting_2020", base+pre, base+pre+"+buyer_rating_2023"]:
    r=smf.ols(f,df).fit(cov_type="HC1"); print(r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
print(df.corr(numeric_only=True)['supplier_diversity'])
