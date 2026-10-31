import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum(), len(df))
print(df.export_growth_2023.describe())
f="export_growth_2023~supplier_diversity"
for c in ["", "+log_sales_2020+years_exporting_2020","+log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"]:
    r=smf.ols(f+c,df).fit(cov_type="HC1"); print(r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
y=df.export_growth_2023;lo,hi=y.quantile([.01,.99]);d=df[(y>=lo)&(y<=hi)]
r=smf.ols(f+"+log_sales_2020+years_exporting_2020",d).fit(cov_type="HC1");print(r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
print(df.corr(numeric_only=True)['supplier_diversity'])
