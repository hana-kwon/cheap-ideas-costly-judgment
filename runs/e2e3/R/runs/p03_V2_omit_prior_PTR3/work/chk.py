import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="export_growth_2023 ~ supplier_diversity + log_sales_2020 + years_exporting_2020"
for name,d in [("all",df),("trim",df[(df.export_growth_2023>=df.export_growth_2023.quantile(.01))&(df.export_growth_2023<=df.export_growth_2023.quantile(.99))])]:
    for ff in [f, f+"+export_growth_2020+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020+C(region)+listed+C(product_group)"]:
        r=smf.ols(ff,d).fit(cov_type="HC1")
        print(name,len(d),r.params['supplier_diversity'],r.bse['supplier_diversity'])
