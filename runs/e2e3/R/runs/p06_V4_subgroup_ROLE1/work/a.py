import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
base="export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020"
ex="+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+listed+C(product_group)+C(region)"
for n,d in [("all",df),("north",df[df.region=="north"])]:
  for f in [base,base+ex,"export_growth_2023~supplier_diversity"]:
    r=smf.ols(f,d).fit(cov_type="HC1");print(n,len(d),f[-20:],r.params['supplier_diversity'],r.bse['supplier_diversity'],r.pvalues['supplier_diversity'])
for g,d in df.groupby("region"):
  r=smf.ols(base+ex.replace("+C(region)",""),d).fit(cov_type="HC1");print(g,len(d),r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
