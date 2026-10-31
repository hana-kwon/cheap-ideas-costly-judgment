import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
specs={"naive":"export_growth_2023~supplier_diversity",
"core":"export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020",
"full_pre":"export_growth_2023~supplier_diversity+"+pre,
"full_pre+buyer(bad)":"export_growth_2023~supplier_diversity+buyer_rating_2023+"+pre,
"full_pre+sq":"export_growth_2023~supplier_diversity+I(supplier_diversity**2)+"+pre,
"full_pre_interact_sector":"export_growth_2023~supplier_diversity*C(product_group)+"+pre}
n=0
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1'); n+=1
    print(k,m.params['supplier_diversity'],m.bse['supplier_diversity'],m.pvalues['supplier_diversity'])
m=smf.ols(specs['full_pre'],d).fit(cov_type='HC1');print(m.summary().tables[1])
# robustness: log outcome? trimmed
d2=d[(d.supplier_diversity.abs()<3)];m=smf.ols(specs['full_pre'],d2).fit(cov_type='HC1');n+=1
print('trim',m.params['supplier_diversity'],m.bse['supplier_diversity'],m.pvalues['supplier_diversity'])
print(n)
