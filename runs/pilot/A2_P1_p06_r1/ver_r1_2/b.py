import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
m=smf.ols('export_growth_2023~supplier_diversity+I(supplier_diversity**2)+'+pre,d).fit(cov_type='HC1')
print(m.summary().tables[1])
d['q']=pd.qcut(d.supplier_diversity,5,labels=False)
print(d.groupby('q').export_growth_2023.mean())
for v in ['region','product_group','listed','foreign_owned','certified_iso']:
    for g,s in d.groupby(v):
        r=smf.ols('export_growth_2023~supplier_diversity+'+pre.replace('C(region)+','').replace('C(product_group)+','') ,s).fit(cov_type='HC1')
        print(v,g,len(s),r.params['supplier_diversity'],r.bse['supplier_diversity'])
