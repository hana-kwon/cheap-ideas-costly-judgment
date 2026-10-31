import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
d['b']=pd.qcut(d.supplier_diversity,5,labels=False)
r=smf.ols('export_growth_2023~C(b)+'+pre,d).fit(cov_type='HC1')
print(r.params[:6]); print(r.bse[:6])
print(smf.ols('export_growth_2023~supplier_diversity*log_sales_2020+supplier_diversity*years_exporting_2020+'+pre,d).fit(cov_type='HC1').summary().tables[1])
print(d.corr(numeric_only=True)['supplier_diversity'])
