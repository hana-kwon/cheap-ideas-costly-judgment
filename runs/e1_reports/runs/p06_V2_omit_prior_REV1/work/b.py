import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
base="export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"
for m in ["", "+I(supplier_diversity**2)"]:
    r=smf.ols(base+m,df).fit(cov_type="HC1");print(r.summary().tables[1])
for v in ["region","product_group","listed","foreign_owned","port_distance_km"]:
    r=smf.ols(base+"+supplier_diversity:C(%s)"%v,df).fit(cov_type="HC1")
    print(v,{k:(round(x,3),round(r.pvalues[k],4)) for k,x in r.params.items() if ':' in k})
for v in ["log_sales_2020","years_exporting_2020","inventory_days_2020","share_imported_inputs_2020","debt_ratio_2020","certified_iso","export_growth_2020"]:
    r=smf.ols(base+"+supplier_diversity:%s"%v,df).fit(cov_type="HC1")
    print(v,{k:(round(x,3),round(r.pvalues[k],4)) for k,x in r.params.items() if ':' in k})
