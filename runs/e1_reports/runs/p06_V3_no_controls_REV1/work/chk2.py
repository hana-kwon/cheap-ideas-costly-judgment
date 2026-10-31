import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
for c in ['log_sales_2020','years_exporting_2020','export_growth_2020']:
    r=smf.ols('export_growth_2023~supplier_diversity+'+c,d).fit(cov_type='HC1');print(c,r.params['supplier_diversity'],r.bse['supplier_diversity'])
