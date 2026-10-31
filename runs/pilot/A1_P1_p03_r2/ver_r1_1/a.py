import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
specs={'raw':'',
'core':'+log_sales_2020+years_exporting_2020+export_growth_2020',
'full_pre':'+'+pre,
'full_pre+rating':'+'+pre+'+buyer_rating_2023'}
for k,v in specs.items():
    m=smf.ols('export_growth_2023~supplier_diversity'+v,d).fit(cov_type='HC1')
    print(k,m.params['supplier_diversity'],m.bse['supplier_diversity'],m.pvalues['supplier_diversity'],int(m.nobs))
m=smf.ols('buyer_rating_2023~supplier_diversity+'+pre,d).fit(cov_type='HC1');print(m.params['supplier_diversity'],m.pvalues['supplier_diversity'])
m=smf.ols('export_growth_2023~supplier_diversity*C(product_group)+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
