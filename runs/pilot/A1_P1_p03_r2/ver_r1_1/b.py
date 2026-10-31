import pandas as pd, statsmodels.formula.api as smf, numpy as np
d=pd.read_csv('data.csv')
print(d.describe().T)
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
m=smf.ols('export_growth_2023~supplier_diversity+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
m=smf.ols('export_growth_2023~supplier_diversity+I(supplier_diversity**2)+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
print(d.corr(numeric_only=True)['supplier_diversity'])
q=d[(d.export_growth_2023>d.export_growth_2023.quantile(.01))&(d.export_growth_2023<d.export_growth_2023.quantile(.99))]
m=smf.ols('export_growth_2023~supplier_diversity+'+pre,q).fit(cov_type='HC1');print(m.params['supplier_diversity'],m.bse['supplier_diversity'])
