import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum(), df.region.value_counts().to_dict())
c="+log_sales_2020+years_exporting_2020+export_growth_2020"
allc=c+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+listed+C(product_group)"
for r in ['north','central','south',None]:
    d=df if r is None else df[df.region==r]
    for ctrl in ["",c,allc]:
        f=smf.ols("export_growth_2023~supplier_diversity"+ctrl,d).fit(cov_type="HC1")
        print(r,len(ctrl),len(d),round(f.params['supplier_diversity'],3),round(f.bse['supplier_diversity'],3),round(f.pvalues['supplier_diversity'],4))
f=smf.ols("export_growth_2023~supplier_diversity*C(region)"+allc,df).fit(cov_type="HC1");print(f.summary().tables[1])
f=smf.ols("export_growth_2023~supplier_diversity+C(region)"+allc,df).fit(cov_type="HC1");print(f.params['supplier_diversity'],f.pvalues['supplier_diversity'])
print(df.export_growth_2023.describe())
