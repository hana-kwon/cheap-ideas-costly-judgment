import pandas as pd, numpy as np, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.describe().T)
print(df.isna().sum().sum())
base="export_growth_2023 ~ supplier_diversity"
cs=["log_sales_2020","years_exporting_2020","export_growth_2020","C(region)","listed","C(product_group)","inventory_days_2020","foreign_owned","share_imported_inputs_2020","port_distance_km","certified_iso","debt_ratio_2020"]
for name,f,d in [("raw",base,df),("size_age",base+"+log_sales_2020+years_exporting_2020",df),("all pre","+".join([base]+cs),df),("all+buyer","+".join([base]+cs+["buyer_rating_2023"]),df)]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(name,r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'],r.nobs)
r=smf.quantreg(base+"+log_sales_2020+years_exporting_2020",df).fit();print("median",r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
for g,d in df.groupby("product_group"):
    r=smf.ols(base+"+log_sales_2020+years_exporting_2020",d).fit(cov_type="HC1");print(g,r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
for g,d in df.groupby("region"):
    r=smf.ols(base,d).fit(cov_type="HC1");print(g,r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
for g,d in df.groupby("listed"):
    r=smf.ols(base,d).fit(cov_type="HC1");print("listed",g,r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
