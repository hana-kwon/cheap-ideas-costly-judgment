import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum(), df.region.value_counts())
f="export_growth_2023~supplier_diversity"
c="+log_sales_2020+years_exporting_2020+export_growth_2020"
for name,d in [("all",df)]+[(r,g) for r,g in df.groupby("region")]:
    for ff in [f,f+c,f+c+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+listed+C(product_group)"]:
        r=smf.ols(ff,d).fit(cov_type="HC1")
        print(name,len(d),len(ff),round(r.params['supplier_diversity'],3),round(r.bse['supplier_diversity'],3),round(r.pvalues['supplier_diversity'],4))
print(df.corr(numeric_only=True)['supplier_diversity'])
