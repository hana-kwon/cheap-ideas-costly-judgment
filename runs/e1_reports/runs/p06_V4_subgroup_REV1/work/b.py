import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
base="export_growth_2023~supplier_diversity"
for c in ['log_sales_2020','years_exporting_2020','export_growth_2020','inventory_days_2020','foreign_owned','share_imported_inputs_2020','port_distance_km','certified_iso','debt_ratio_2020','listed','C(region)','C(product_group)','buyer_rating_2023']:
    m=smf.ols(base+"+"+c,df).fit(cov_type="HC1");print(c,round(m.params['supplier_diversity'],3),round(m.bse['supplier_diversity'],3))
print(df.corr(numeric_only=True)['supplier_diversity'])
for g in ['durables','nondurables']:
    d=df[df.product_group==g]
    m=smf.ols("export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+C(region)",d).fit(cov_type="HC1");print(g,m.params['supplier_diversity'],m.bse['supplier_diversity'])
