import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
c=" + log_sales_2020+years_exporting_2020+export_growth_2020"
c2=c+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(product_group)+listed"
for n,d in [("all",df)]+[(r,df[df.region==r]) for r in ['north','central','south']]:
    for cc in ["",c,c2]:
        f=smf.ols("export_growth_2023~supplier_diversity"+cc,d).fit(cov_type="HC1")
        print(n,len(d),len(cc),round(f.params['supplier_diversity'],3),round(f.bse['supplier_diversity'],3),round(f.pvalues['supplier_diversity'],4))
print(df.isna().sum().sum(), df.export_growth_2023.describe())
