import pandas as pd, numpy as np, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T); print(d.isna().sum().sum())
print(d.corr(numeric_only=True)['supplier_diversity'])
pre="log_sales_2020+years_exporting_2020+export_growth_2020"
oth="inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
cat="C(region)+listed+C(product_group)"
specs={
'raw':'export_growth_2023~supplier_diversity',
'pre':f'export_growth_2023~supplier_diversity+{pre}',
'pre+cat':f'export_growth_2023~supplier_diversity+{pre}+{cat}',
'full_pre':f'export_growth_2023~supplier_diversity+{pre}+{cat}+{oth}',
'full+rating(bad)':f'export_growth_2023~supplier_diversity+{pre}+{cat}+{oth}+buyer_rating_2023',
'full+quad':f'export_growth_2023~supplier_diversity+{pre}+{cat}+{oth}+I(log_sales_2020**2)+I(export_growth_2020**2)',
}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,round(m.params['supplier_diversity'],3),round(m.bse['supplier_diversity'],3),m.pvalues['supplier_diversity'],len(m.params))
m=smf.ols(specs['full_pre'],d).fit(cov_type='HC1');print(m.summary())
m=smf.ols(specs['full_pre'],d).fit(cov_type='cluster',cov_kwds={'groups':d.region.astype('category').cat.codes});
# robust: winsorized outcome
d2=d.copy();lo,hi=d.export_growth_2023.quantile([.01,.99]);d2['export_growth_2023']=d.export_growth_2023.clip(lo,hi)
m=smf.ols(specs['full_pre'],d2).fit(cov_type='HC1');print('wins',m.params['supplier_diversity'],m.bse['supplier_diversity'],m.pvalues['supplier_diversity'])
