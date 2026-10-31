import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
pre="log_sales_2020+years_exporting_2020+export_growth_2020"
pre2=pre+"+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"
for f in ["export_growth_2023~supplier_diversity","export_growth_2023~supplier_diversity+"+pre,"export_growth_2023~supplier_diversity+"+pre2,"export_growth_2023~supplier_diversity+"+pre+"+buyer_rating_2023","export_growth_2023~supplier_diversity+"+pre2+"+buyer_rating_2023","buyer_rating_2023~supplier_diversity+"+pre2]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(f[-40:],r.params["supplier_diversity"],r.bse["supplier_diversity"])
