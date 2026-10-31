import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
print(d.isna().sum().sum(), d.describe().T)
print(d.corr(numeric_only=True)['supplier_diversity'])
base='export_growth_2023~supplier_diversity'
pre='+log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020'
for f in [base,base+pre,base+pre+'+buyer_rating_2023']:
    print(smf.ols(f,d).fit(cov_type='HC1').summary().tables[1])
print(open('analysis.py').read())
