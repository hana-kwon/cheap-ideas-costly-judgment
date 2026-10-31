import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.isna().sum().sum())
base="export_growth_2023 ~ supplier_diversity"
c=" + log_sales_2020+years_exporting_2020+export_growth_2020"
allc=c+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+listed+C(product_group)+C(region)"
for name,d in [("all",df)]+[(r,df[df.region==r]) for r in ['north','central','south']]:
    for f in [base,base+c,base+allc]:
        if name!='all': f=f.replace("+C(region)","")
        m=smf.ols(f,d).fit(cov_type="HC1")
        print(name,len(d),f[-12:],round(m.params['supplier_diversity'],3),round(m.bse['supplier_diversity'],3),round(m.pvalues['supplier_diversity'],4))
y=df.export_growth_2023;lo,hi=y.quantile([.01,.99]);d=df[(y>=lo)&(y<=hi)]
m=smf.ols(base+allc,d).fit(cov_type="HC1");print("trim all",m.params['supplier_diversity'],m.pvalues['supplier_diversity'])
print(df.groupby('region').supplier_diversity.mean())
print(df[['supplier_diversity','export_growth_2023']].describe())
