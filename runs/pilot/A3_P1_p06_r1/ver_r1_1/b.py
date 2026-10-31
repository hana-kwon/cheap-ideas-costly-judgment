import pandas as pd, statsmodels.formula.api as smf, numpy as np
d=pd.read_csv('data.csv')
print(d.isna().sum().sum()); print(d.describe().T)
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
m=smf.ols("export_growth_2023~supplier_diversity+I(supplier_diversity**2)+"+pre,d).fit(cov_type='HC1')
print(m.summary().tables[1])
for c in ['region','product_group','listed','foreign_owned','certified_iso']:
    for k,g in d.groupby(c):
        f="export_growth_2023~supplier_diversity+"+pre
        f=f.replace("C(%s)+"%c,"").replace("+%s+"%c,"+")
        r=smf.ols(f,g).fit(cov_type='HC1')
        print(c,k,len(g),r.params['supplier_diversity'],r.bse['supplier_diversity'])
print(d.corr(numeric_only=True).round(2))
