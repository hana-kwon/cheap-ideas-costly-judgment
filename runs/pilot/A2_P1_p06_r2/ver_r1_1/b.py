import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.describe().T)
c="+log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
for f in ["export_growth_2023~supplier_diversity","export_growth_2023~supplier_diversity"+c,"export_growth_2023~supplier_diversity+I(supplier_diversity**2)"+c,"export_growth_2023~supplier_diversity*C(product_group)"+c,"export_growth_2023~supplier_diversity*C(region)"+c,"export_growth_2023~supplier_diversity*listed"+c]:
    r=smf.ols(f,d).fit(cov_type='HC1');print(f[:60]);print(r.params.filter(regex='supplier'),r.pvalues.filter(regex='supplier'))
print(d.corr(numeric_only=True)['supplier_diversity'])
