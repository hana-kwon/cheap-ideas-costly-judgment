import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
m=smf.ols('export_growth_2023~supplier_diversity+'+pre,d).fit(cov_type='HC1');print(m.summary().tables[1])
print(d.export_growth_2023.describe())
pre2="log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
for g in ['region','product_group','listed']:
    for k,s in d.groupby(g):
        r=smf.ols('export_growth_2023~supplier_diversity+'+pre2,s).fit();print(g,k,r.params['supplier_diversity'],r.bse['supplier_diversity'])
m2=smf.ols('export_growth_2023~supplier_diversity+I(supplier_diversity**2)+I(supplier_diversity**3)+'+pre,d).fit(cov_type='HC1');print(m2.params.filter(like='supplier'),m2.pvalues.filter(like='supplier'))
print(d.corr(numeric_only=True).round(2).to_string())
