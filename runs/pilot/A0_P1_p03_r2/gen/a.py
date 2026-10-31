import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T[['count','mean','std']]); print(d.isna().sum().sum())
pre="log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+listed+C(region)+C(product_group)"
S={'raw':'',
'pre_basic':'log_sales_2020+years_exporting_2020+export_growth_2020',
'pre_full':pre,
'pre_full+buyer_rating(post)':pre+'+buyer_rating_2023',
'raw+buyer_rating(post)':'buyer_rating_2023'}
for k,v in S.items():
    f='export_growth_2023~supplier_diversity'+('+'+v if v else '')
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,round(m.params['supplier_diversity'],4),round(m.bse['supplier_diversity'],4),m.pvalues['supplier_diversity'],m.nobs)
m=smf.ols('export_growth_2023~supplier_diversity+'+pre,d).fit(cov_type='HC1')
print(m.summary())
m=smf.ols('export_growth_2023~supplier_diversity*C(product_group)+'+pre,d).fit(cov_type='HC1')
print(m.params.filter(like='supplier'),m.pvalues.filter(like='supplier'))
print(d.corr(numeric_only=True)['supplier_diversity'])
