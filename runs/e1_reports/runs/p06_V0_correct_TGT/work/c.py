import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="log_sales_2020+years_exporting_2020+export_growth_2020"
allc=pre+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"
for n,f in [("none","export_growth_2023~supplier_diversity"),("pre","export_growth_2023~supplier_diversity+"+pre),("all","export_growth_2023~supplier_diversity+"+allc)]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(n,r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'],int(r.nobs))
lo,hi=df.export_growth_2023.quantile([.01,.99]);d=df[(df.export_growth_2023>=lo)&(df.export_growth_2023<=hi)]
r=smf.ols("export_growth_2023~supplier_diversity+"+allc,d).fit(cov_type="HC1");print("trim all",r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
