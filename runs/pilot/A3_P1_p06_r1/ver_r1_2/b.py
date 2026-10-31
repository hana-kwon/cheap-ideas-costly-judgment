import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
m=smf.ols("export_growth_2023~supplier_diversity+I(supplier_diversity**2)+"+pre,d).fit(cov_type='HC1')
print(m.summary().tables[1])
for c in ['log_sales_2020','years_exporting_2020','export_growth_2020','inventory_days_2020','foreign_owned','share_imported_inputs_2020','port_distance_km','certified_iso','debt_ratio_2020','listed']:
    m=smf.ols("export_growth_2023~supplier_diversity+"+c,d).fit(cov_type='HC1')
    print(c,m.params['supplier_diversity'],m.pvalues['supplier_diversity'])
print(d.corr(numeric_only=True).round(2))
for g in ['region','product_group']:
    for k,s in d.groupby(g):
        m=smf.ols("export_growth_2023~supplier_diversity+"+pre.replace("C(region)+","").replace("C(product_group)+",""),s).fit()
        print(g,k,m.params['supplier_diversity'],m.pvalues['supplier_diversity'])
