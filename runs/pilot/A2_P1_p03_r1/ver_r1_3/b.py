import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
for c in ['product_group','region']:
    for g,s in d.groupby(c):
        m=smf.ols('export_growth_2023~supplier_diversity+'+pre,s).fit(cov_type='HC1');print(g,m.params['supplier_diversity'],m.bse['supplier_diversity'])
m=smf.ols('export_growth_2023~supplier_diversity+I(supplier_diversity**2)+'+pre,d).fit(cov_type='HC1');print(m.pvalues[['supplier_diversity','I(supplier_diversity ** 2)']])
print(d[['supplier_diversity','log_sales_2020','years_exporting_2020','export_growth_2020']].corr())
