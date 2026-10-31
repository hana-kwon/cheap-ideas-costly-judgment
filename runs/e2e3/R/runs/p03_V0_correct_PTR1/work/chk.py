import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
lo,hi=d.export_growth_2023.quantile([.01,.99])
t=d[(d.export_growth_2023>=lo)&(d.export_growth_2023<=hi)]
for n,x in [('all',d),('trim',t)]:
    for f in ['export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020','export_growth_2023~supplier_diversity+'+pre]:
        m=smf.ols(f,x).fit(cov_type='HC1');print(n,m.params['supplier_diversity'],m.bse['supplier_diversity'],m.pvalues['supplier_diversity'],m.nobs)
