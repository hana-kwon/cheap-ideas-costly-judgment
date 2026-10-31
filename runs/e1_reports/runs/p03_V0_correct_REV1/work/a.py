import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum(), df.describe().T[['mean','std','min','max']])
base="export_growth_2023~supplier_diversity"
pre="+log_sales_2020+years_exporting_2020+export_growth_2020"
allp=pre+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"
for n,f in [("raw",base),("pre",base+pre),("all",base+allp),("allpost",base+allp+"+buyer_rating_2023")]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(n,r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
print(df[['supplier_diversity','inventory_days_2020','foreign_owned','share_imported_inputs_2020','port_distance_km','certified_iso','debt_ratio_2020','log_sales_2020','export_growth_2023']].corr().round(2))
