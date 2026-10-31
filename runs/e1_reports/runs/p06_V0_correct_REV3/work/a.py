import pandas as pd, statsmodels.formula.api as smf, numpy as np
df=pd.read_csv("data.csv")
f="export_growth_2023~supplier_diversity"
for c in ["","+log_sales_2020","+years_exporting_2020","+export_growth_2020","+inventory_days_2020","+foreign_owned","+share_imported_inputs_2020","+port_distance_km","+certified_iso","+debt_ratio_2020","+C(region)","+listed","+C(product_group)","+buyer_rating_2023"]:
    r=smf.ols(f+c,df).fit(cov_type="HC1");print(c,round(r.params['supplier_diversity'],3),round(r.bse['supplier_diversity'],3))
print(df.corr(numeric_only=True).round(2).to_string())
r=smf.ols(f+"+I(supplier_diversity**2)+log_sales_2020+export_growth_2020+years_exporting_2020",df).fit(cov_type="HC1");print(r.summary().tables[1])
r=smf.ols(f+"*C(region)+log_sales_2020+export_growth_2020+years_exporting_2020",df).fit(cov_type="HC1");print(r.summary().tables[1])
