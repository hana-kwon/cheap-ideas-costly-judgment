import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre='log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020'
m=smf.ols('export_growth_2023~supplier_diversity+I(supplier_diversity**2)+'+pre,d).fit(cov_type='HC1')
print(m.summary().tables[1])
for v in ['listed','product_group','region','foreign_owned','certified_iso']:
    m=smf.ols(f'export_growth_2023~supplier_diversity*C({v})+'+pre,d).fit(cov_type='HC1')
    print(v,m.params.filter(like='supplier_diversity:').round(3).to_dict(),m.pvalues.filter(like='supplier_diversity:').round(3).to_dict())
print(d.corr(numeric_only=True).round(2)['supplier_diversity'])
print(d.export_growth_2023.describe())
