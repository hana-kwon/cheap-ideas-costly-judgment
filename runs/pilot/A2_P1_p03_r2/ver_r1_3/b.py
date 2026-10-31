import pandas as pd, statsmodels.formula.api as smf, numpy as np
d=pd.read_csv('data.csv')
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
print(d[['supplier_diversity','buyer_rating_2023','export_growth_2023','log_sales_2020','export_growth_2020']].corr().round(2))
m=smf.ols('export_growth_2023~supplier_diversity+I(supplier_diversity**2)+'+pre,d).fit(cov_type='HC1');print(m.params[:6],m.pvalues[:6])
for g,s in d.groupby('product_group'): print(g,smf.ols('export_growth_2023~supplier_diversity+'+pre,s).fit().params['supplier_diversity'])
for g,s in d.groupby('region'): print(g,smf.ols('export_growth_2023~supplier_diversity+'+pre,s).fit().params['supplier_diversity'])
