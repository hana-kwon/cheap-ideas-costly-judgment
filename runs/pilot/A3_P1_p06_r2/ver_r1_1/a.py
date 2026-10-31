import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T[['count','mean','std','min','max']])
print(d.isna().sum().sum())
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
specs={'naive':'export_growth_2023~supplier_diversity',
'pre_controls':'export_growth_2023~supplier_diversity+'+pre,
'pre+rating(bad control)':'export_growth_2023~supplier_diversity+buyer_rating_2023+'+pre,
'minimal':'export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020',
'quadratic':'export_growth_2023~supplier_diversity+I(supplier_diversity**2)+'+pre}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['supplier_diversity'],m.bse['supplier_diversity'],m.pvalues['supplier_diversity'],m.nobs)
m=smf.ols(specs['pre_controls'],d).fit(cov_type='HC1');print(m.summary())
print(d[['supplier_diversity','buyer_rating_2023','export_growth_2023']].corr())
