import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="log_sales_2020+years_exporting_2020+export_growth_2020"
allp=pre+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
for name,d in [("all",df),("north",df[df.region=="north"])]:
  for f in ["1",pre,allp,allp+"+C(region)+C(product_group)+listed"]:
    r=smf.ols("export_growth_2023~supplier_diversity+"+f,d).fit(cov_type="HC1")
    print(name,len(d),f[:30],r.params.supplier_diversity,r.bse.supplier_diversity,r.pvalues.supplier_diversity)
print(df.region.value_counts())
for g,d in df.groupby("region"):
    r=smf.ols("export_growth_2023~supplier_diversity+"+allp,d).fit(cov_type="HC1");print(g,r.params.supplier_diversity,r.pvalues.supplier_diversity)
