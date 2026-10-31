import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.isna().sum().sum(), d.describe().T)
for f in ['export_growth_2023 ~ supplier_diversity','export_growth_2023 ~ supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020']:
    for dd in [d, d[d.export_growth_2023.between(*d.export_growth_2023.quantile([.01,.99]))]]:
        r=smf.ols(f,dd).fit(cov_type='HC1');print(r.params['supplier_diversity'],r.bse['supplier_diversity'])
print(d.corr(numeric_only=True)['supplier_diversity'])
