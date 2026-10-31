import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
pre="log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+listed"
specs={
'naive':'export_growth_2023~supplier_diversity',
'pre_controls':f'export_growth_2023~supplier_diversity+{pre}',
'pre_controls_fe':f'export_growth_2023~supplier_diversity+{pre}+C(region)+C(product_group)',
'with_buyer_rating(bad control)':f'export_growth_2023~supplier_diversity+{pre}+C(region)+C(product_group)+buyer_rating_2023',
'minimal':'export_growth_2023~supplier_diversity+log_sales_2020+export_growth_2020',
'quad':f'export_growth_2023~supplier_diversity+I(supplier_diversity**2)+{pre}+C(region)+C(product_group)',
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['supplier_diversity'],m.bse['supplier_diversity'],m.pvalues['supplier_diversity'],m.nobs)
m=smf.ols(specs['pre_controls_fe'],d).fit(cov_type='HC1');print(m.summary())
